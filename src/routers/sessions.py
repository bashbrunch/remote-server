from fastapi import APIRouter, Request, Response

from src.core.session import (
  create_session,
  delete_session,
  get_session,
  is_available_session,
)

_router = APIRouter(tags=["sessions"])

class SessionsRouter:
  router = _router

_get = _router.get
_post = _router.post
_delete = _router.delete

@_post("")
async def start_session(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  available = is_available_session(session_id, session_key)

  if not available:
    return Response("access denied", 403)

  content_bytes = await request.body()
  new_session_key = content_bytes.decode()
  create_session(session_id, new_session_key)

  return Response("ok", 200)

@_get("")
async def check_session(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  return Response("ok", 200)

@_delete("")
async def close_session(session_id: str, request: Request):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    return Response("access denied", 403)

  delete_session(session_id, session_key)

  return Response("ok", 200)

