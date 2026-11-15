from fastapi import APIRouter, Request, Response

from src.models.session import Session

_router = APIRouter(tags=["proxies"])

class ProxiesRouter:
  router = _router

_get = _router.get
_post = _router.post
_delete = _router.delete

@_post("")
async def send_proxies(request: Request):
  session: Session = request.state.session
  content_bytes = await request.body()
  content = content_bytes.decode()

  if not content:
    return Response("body required", 400)

  session.push("proxies", content)

  return Response("ok", 200)

@_get("")
async def get_proxies(request: Request):
  session: Session = request.state.session
  message = session.seek("proxies")

  if not message:
    return Response("missing", 404)

  return Response(message, 200)

@_delete("/{key}")
async def pop_proxies(key: str, request: Request):
  session: Session = request.state.session
  exists, polled = session.poll("proxies", key)

  if not exists:
    return Response("missing", 404)

  if not polled:
    return Response("key mismatch", 400)

  return Response("ok", 200)

