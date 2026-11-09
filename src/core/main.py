from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse

from src.core.cors import cors_middleware

from src.core.session import (
  get_session,
  create_session,
  is_available_session,
  delete_session,
)

app = FastAPI()
app.middleware("https")(cors_middleware)

@app.get("/")
async def home():
  return "Hello, Brunch OTN Server"

@app.post("/{session_id}")
async def start_session(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  available = is_available_session(session_id, session_key)

  if not available:
    return Response("access denied", 403)

  content_bytes = await request.body()
  new_session_key = content_bytes.decode()
  create_session(session_id, new_session_key)

  return Response("ok", 200)

@app.get("/{session_id}")
async def check_session(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  return Response("ok", 200)

@app.delete("/{session_id}")
async def close_session(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  delete_session(session_id, session_key)

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
  session.push_log(content)

  return Response("ok", 200)

@app.get("/{session_id}/logs")
async def get_logs(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  return StreamingResponse(
    session.stream_logs(),
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

  session.push_message(content)

  return Response("ok", 200)

@app.get("/{session_id}/message")
async def get_message(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  message = session.seek_message()

  if not message:
    return Response("missing", 404)

  return Response(message, 200)

@app.delete("/{session_id}/message/{key}")
async def pop_message(session_id: str, key: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  exists, polled = session.poll_message(key)

  if not exists:
    return Response("missing", 404)

  if not polled:
    return Response("key mismatch", 400)

  return Response("ok", 200)

