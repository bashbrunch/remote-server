from fastapi import APIRouter, Depends

from src.intermediates.sessions import session_authenticate
from src.models.session import Session
from src.routers.factories.queue import QueueRouterFactory
from src.routers.logs import LogsRouter
from src.routers.sessions import SessionsRouter

_router = APIRouter(prefix="/{session_id}")

class IndexRouter:
  router = _router

def add_queue_router(label: str):
  _router.include_router(
    QueueRouterFactory.generate(label),
    prefix=f"/{label}",
    dependencies=[
      Depends(session_authenticate),
    ],
  )

_router.include_router(
  SessionsRouter.router,
  prefix="/sessions",
)

_router.include_router(
  LogsRouter.router,
  prefix="/logs",
  dependencies=[Depends(session_authenticate)],
)

for label in Session.labels:
  add_queue_router(label)

