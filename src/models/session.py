from src.core.cache import Cache
from src.utils import generate_key

class Session:
  id: str = ""

  def __init__(self, session_id: str):
    self.id = session_id

  def auth_check(self, session_key: str) -> bool:
    key = Cache.get(f"{self.id}:key")

    if not key:
      return True

    return key == session_key

  def auth_set(self, session_key: str):
    Cache.set(f"{self.id}:key", session_key)

  def push_log(self, log: str):
    chunk_idx = int(Cache.get(f"{self.id}:idx", "0"))
    chunk_data = Cache.get(f"{self.id}:{chunk_idx}")
    chunk_data += f"{log}\n"

    if len(chunk_data) > 1024 * 1024:
      chunk_idx += 1
      chunk_data = f"{log}\n"

    Cache.set(f"{self.id}:idx", str(chunk_idx))
    Cache.set(f"{self.id}:{chunk_idx}", chunk_data)

  def stream_logs(self):
    idx = int(Cache.get(f"{self.id}:idx", "0"))

    while idx >= 0:
      data = Cache.get(f"{self.id}:{idx}")
      idx -= 1

      yield data

  def push_message(self, content: str):
    msg_id = generate_key()
    Cache.set(f"{self.id}::{msg_id}", content)
    _buffer = Cache.get(f"{self.id}:buffer", "")
    _buffer += f"{msg_id}\n"
    Cache.set(f"{self.id}:buffer", _buffer)

  def seek_message(self) -> str | None:
    _buffer = Cache.get(f"{self.id}:buffer")
    splits = _buffer.split("\n", 1)

    if not splits or not splits[0]:
      return None

    key = splits[0]
    message = Cache.get(f"{self.id}::{key}")

    return f"{key}\n{message}"

  def poll_message(self, key: str) -> tuple[bool, bool]:
    _buffer = Cache.get(f"{self.id}:buffer")

    if not _buffer:
      return False, False

    splits = _buffer.split("\n", 1)

    if not splits or not splits[0]:
      return False, False

    if splits[0] != key:
      return True, False

    Cache.delete(f"{self.id}::{key}")

    if len(splits) > 1:
      Cache.set(f"{self.id}:buffer", splits[1])
    else:
      Cache.delete(f"{self.id}:buffer")

    return True, True

  def destroy(self):
    _buffer = Cache.get(f"{self.id}:buffer")
    keys = _buffer.split("\n") if _buffer else []

    for key in keys:
      if not key: continue
      Cache.delete(f"{self.id}::{key}")

    idx = 0

    while Cache.get(f"{self.id}:{idx}"):
      Cache.delete(f"{self.id}:{idx}")
      idx += 1

    Cache.delete(f"{self.id}:idx")
    Cache.delete(f"{self.id}:key")
    Cache.delete(f"{self.id}:buffer")

