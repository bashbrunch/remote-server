from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse

_router = APIRouter(tags=["logs"])

class LogsRouter:
  router = _router

_get = _router.get
_post = _router.post

@_post("")
async def send_logs(request: Request):
  session = request.state.session
  content_bytes = await request.body()
  content = content_bytes.decode()
  session.push_log(content)

  return Response("ok", 200)

@_get("")
async def get_logs(request: Request):
  session = request.state.session

  return StreamingResponse(
    session.stream_logs(),
    media_type="text/plain",
  )

