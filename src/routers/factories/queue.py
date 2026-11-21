from fastapi import APIRouter, Request, Response

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

    send.__name__ = f"send_{label}"
    seek.__name__ = f"seek_{label}"
    poll.__name__ = f"poll_{label}"

    def add_routes():
      router.post("")(send)
      router.get("")(seek)
      router.delete("/{key}")(poll)

    add_routes()

    return router

