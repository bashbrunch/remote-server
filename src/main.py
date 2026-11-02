from random import randint

from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse

from src.cors import cors_middleware

app = FastAPI()
app.middleware("https")(cors_middleware)
content_map: dict[str, str] = {}
content_queue: list[str] = []
logs: list[str] = []

@app.get("/")
async def home():
  return "Hello, Brunch OTN Server"

@app.post("/shell")
async def send_shell(request: Request):
  content_bytes = await request.body()
  content = content_bytes.decode()
  logs.append(f"{content}\n")

  return Response("ok", 200)

@app.get("/shell")
async def get_shell():
  if not logs:
    return Response("no log", 404)

  def log_stream():
    line = len(logs) - 1

    while line >= 0:
      yield logs[line] + "\n"
      line -= 1

  return StreamingResponse(
    log_stream(),
    media_type="text/plain",
  )

@app.post("/message")
async def send_message(request: Request):
  content_bytes = await request.body()
  content = content_bytes.decode()
  key = hex(randint(1 << 63, 1 << 64))[2:]

  if not content:
    return Response("body required", 400)

  content_queue.append(key)
  content_map[key] = content

  return Response("added", 200)

@app.get("/message")
async def get_message():
  if not content_queue:
    return Response("no message", 404)

  key = content_queue[0]
  content = content_map[key]

  return Response(f"{key}\n{content}", 200)

@app.delete("/message/{key}")
async def pop_message(key: str):
  if not content_queue:
    return Response("key mismatch", 400)

  if key != content_queue[0]:
    return Response("key mismatch", 400)

  content_queue.pop(0)
  del content_map[key]

  return Response("deleted", 200)

