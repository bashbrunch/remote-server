from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse

from src.core.session import get_session

_router = APIRouter(tags=["logs"])

class LogsRouter:
  router = _router

_get = _router.get
_post = _router.post

@_post("")
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

@_get("")
async def get_logs(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  return StreamingResponse(
    session.stream_logs(),
    media_type="text/plain",
  )

