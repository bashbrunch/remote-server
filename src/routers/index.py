from fastapi import APIRouter, Depends, Request, HTTPException

from src.core.session import get_session
from src.routers.logs import LogsRouter
from src.routers.messages import MessagesRouter
from src.routers.sessions import SessionsRouter

async def authenticate_session(
  session_id: str,
  request: Request
):
  session_key = request.headers.get("Authorization", "")
  session = get_session(session_id, session_key)

  if not session:
    raise HTTPException(status_code=403, detail="access denied")

  request.state.session = session

_router = APIRouter(prefix="/{session_id}")

class IndexRouter:
  router = _router

_router.include_router(
  SessionsRouter.router,
  prefix="/sessions",
)

_router.include_router(
  MessagesRouter.router,
  prefix="/messages",
  dependencies=[Depends(authenticate_session)]
)

_router.include_router(
  LogsRouter.router,
  prefix="/logs",
  dependencies=[Depends(authenticate_session)]
)

