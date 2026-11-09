from random import randint

from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse

from src.cors import cors_middleware

def generate_key() -> str:
  return hex(randint(1 << 63, 1 << 64))[2:]

app = FastAPI()
app.middleware("https")(cors_middleware)

class Message:
  key: str
  content: str

  def __init__(self, content: str):
    self.key = generate_key()
    self.content = content

class Session:
  key: str | None = None
  buffer: list[Message] = []
  logs: list[str] = []

sessions: dict[str, Session] = {}

def get_session(
  session_id: str,
  session_key: str,
) -> Session | None:
  if session_id not in sessions:
    return None

  session = sessions[session_id]

  if session.key and session.key != session_key:
    return None

  return session

@app.get("/")
async def home():
  return "Hello, Brunch OTN Server"

@app.post("/{session_id}")
async def start_session(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session and session_id in sessions:
    return Response("access denied", 403)
  
  content_bytes = await request.body()
  new_session_key = content_bytes.decode()

  sessions[session_id] = Session()
  sessions[session_id].key = new_session_key

  if not new_session_key:
    sessions[session_id].key = None

  return Response("ok", 200)

@app.get("/{session_id}")
async def check_session(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  return Response("ok", 200)

@app.delete("/{session_id}")
async def delete_session(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  del sessions[session_id]

  return Response("ok", 200)

@app.post("/{session_id}/logs")
async def send_logs(
  session_id: str,
  request: Request,
):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  content_bytes = await request.body()
  content = content_bytes.decode()
  session.logs.append(f"{content}\n")

  return Response("ok", 200)

@app.get("/{session_id}/logs")
async def get_logs(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  if not session.logs:
    return Response("missing", 404)

  def log_stream():
    line = len(session.logs) - 1

    while line >= 0:
      yield session.logs[line] + "\n"
      line -= 1

  return StreamingResponse(
    log_stream(),
    media_type="text/plain",
  )

@app.post("/{session_id}/message")
async def send_message(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  content_bytes = await request.body()
  content = content_bytes.decode()

  if not content:
    return Response("body required", 400)

  session.buffer.append(Message(content))

  return Response("ok", 200)

@app.get("/{session_id}/message")
async def get_message(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  if not session.buffer:
    return Response("missing", 404)

  message = session.buffer[0]
  key = message.key
  content = message.content

  return Response(f"{key}\n{content}", 200)

@app.delete("/{session_id}/message/{key}")
async def pop_message(session_id: str, key: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  if not session.buffer:
    return Response("missing", 404)

  if key != session.buffer[0].key:
    return Response("key mismatch", 400)

  session.buffer.pop(0)

  return Response("ok", 200)

