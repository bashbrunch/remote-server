from fastapi import APIRouter, Request, Response

from src.core.session import get_session

_router = APIRouter(tags=["messages"])

class MessagesRouter:
  router = _router

_get = _router.get
_post = _router.post
_delete = _router.delete

@_post("")
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

@_get("")
async def get_message(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  message = session.seek_message()

  if not message:
    return Response("missing", 404)

  return Response(message, 200)

@_delete("")
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

