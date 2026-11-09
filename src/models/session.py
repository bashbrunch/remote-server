from src.models.message import Message

class Session:
  key: str | None = None
  _buffer: list[Message] = []
  _logs: list[str] = []

  def push_log(self, log: str):
    self._logs.append(f"{log}\n")

  def stream_logs(self):
    line = len(self._logs) - 1

    if len(self._logs) == 0:
      yield "no logs\n"
      return

    while line >= 0:
      yield self._logs[line] + "\n"
      line -= 1

  def push_message(self, content: str):
    self._buffer.append(Message(content))

  def seek_message(self) -> str | None:
    if not self._buffer:
      return None

    message = self._buffer[0]

    return message.read()

  def poll_message(self, key: str) -> tuple[bool, bool]:
    if not self._buffer:
      return False, False

    if self._buffer[0].key != key:
      return True, False

    self._buffer.pop(0)

    return True, True

