from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse

from src.models.session import Session

class QueueRouterFactory:
  @staticmethod
  def generate(label: str) -> APIRouter:
    router = APIRouter(tags=[label])

    async def send(request: Request):
      session: Session = request.state.session
      content_bytes = await request.body()
      content = content_bytes.decode()

      if not content:
        return Response("body required", 400)

      await session.queue_push(label, content)

      return Response("ok", 200)

    async def seek(request: Request):
      session: Session = request.state.session
      seeked = await session.queue_seek(label)

      if not seeked:
        return Response("missing", 404)

      return Response(seeked, 200)

    async def poll(key: str, request: Request):
      session: Session = request.state.session
      exists, polled = await session.queue_poll(label, key)

      if not exists:
        return Response("missing", 404)

      if not polled:
        return Response("key mismatch", 400)

      return Response("ok", 200)

    async def keys(request: Request):
      session: Session = request.state.session
      content = await session.queue_list(label)

      return Response(content, 200)

    async def read(request: Request, key: str):
      session: Session = request.state.session
      content = await session.queue_read(label, key)

      if not content:
        return Response("key mismatch", 404)

      return Response(content, 200)

    async def stream(request: Request):
      session: Session = request.state.session

      return StreamingResponse(
        session.queue_stream(label),
        media_type="text/plain",
      )

    apis = [
      send, seek, poll, keys, read, stream
    ]

    for api in apis:
      api.__name__ = f"{label}_{api.__name__}"

    router.post("")(send)
    router.get("")(seek)
    router.get("/keys")(keys)
    router.get("/stream")(stream)
    router.get("/{key}")(read)
    router.delete("/{key}")(poll)

    return router

