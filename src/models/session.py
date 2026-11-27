from src.core.cache import Cache
from src.utils import generate_key

class Session:
  id: str = ""
  labels = {
    "logs",
    "messages",
    "proxies",
    "prompts",
  }

  def __init__(self, session_id: str):
    self.id = session_id

  async def auth_check(self, session_key: str) -> bool:
    key = await Cache.get(f"{self.id}:key")

    if not key:
      return True

    return key == session_key

  async def auth_set(self, session_key: str):
    await Cache.set(f"{self.id}:key", session_key)

  async def queue_push(self, label: str, content: str):
    msg_id = generate_key()
    await Cache.set(f"{self.id}:{label}:{msg_id}", content)
    _buffer = await Cache.get(f"{self.id}:{label}:buffer", "")
    _buffer += f"{msg_id}\n"
    await Cache.set(f"{self.id}:{label}:buffer", _buffer)

  async def queue_read(self, label: str, key: str) -> str:
    return await Cache.get(f"{self.id}:{label}:{key}")

  async def queue_list(self, label: str) -> str:
    return await Cache.get(f"{self.id}:{label}:buffer", "")

  async def queue_seek(self, label: str) -> str | None:
    _buffer = await Cache.get(f"{self.id}:{label}:buffer")
    splits = _buffer.split("\n", 1)

    if not splits or not splits[0]:
      return None

    key = splits[0]
    message = await Cache.get(f"{self.id}:{label}:{key}")

    return f"{key}\n{message}"

  async def queue_stream(self, label: str):
    _buffer = await Cache.get(f"{self.id}:{label}:buffer")
    splits = _buffer.split("\n")

    for key in splits:
      if not key: continue
      yield await Cache.get(f"{self.id}:{label}:{key}") + "\n"

  async def queue_poll(
    self,
    label: str,
    key: str,
  ) -> tuple[bool, bool]:
    _buffer = await Cache.get(f"{self.id}:{label}:buffer")

    if not _buffer:
      return False, False

    splits = _buffer.split("\n", 1)

    if not splits or not splits[0]:
      return False, False

    if splits[0] != key:
      return True, False

    await Cache.delete(f"{self.id}:{label}:{key}")

    if len(splits) > 1:
      await Cache.set(f"{self.id}:{label}:buffer", splits[1])
    else:
      await Cache.delete(f"{self.id}:{label}:buffer")

    return True, True

  async def _queue_clear(self, label: str):
    _buffer = await Cache.get(f"{self.id}:{label}:buffer")
    keys = _buffer.split("\n") if _buffer else []

    for key in keys:
      if not key: continue
      await Cache.delete(f"{self.id}:{label}:{key}")

    await Cache.delete(f"{self.id}:{label}:buffer")

  async def destroy(self):
    idx = 0

    while await Cache.get(f"{self.id}:{idx}"):
      await Cache.delete(f"{self.id}:{idx}")
      idx += 1

    await Cache.delete(f"{self.id}:idx")
    await Cache.delete(f"{self.id}:key")

    for label in self.labels:
      await self._queue_clear(label)

