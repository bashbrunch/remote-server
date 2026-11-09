from src.utils import generate_key

class Message:
  key: str
  _content: str

  def __init__(self, content: str):
    self.key = generate_key()
    self._content = content

  def read(self) -> str:
    return f"{self.key}\n{self._content}"

