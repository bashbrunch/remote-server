from redis import Redis

from src.core.config import Config

_instance: Redis = Redis.from_url(Config.REDIS_URL)

class Cache:
  @staticmethod
  def get(key: str, default: str = "") -> str:
    raw = _instance.get(key)

    if raw is None:
      return default

    data: str = ""

    if isinstance(raw, bytes):
      data = raw.decode()
    else:
      data = str(raw)

    return data

  @staticmethod
  def set(key: str, value: str, ex: int | None = None) -> None:
    _instance.set(key, value, ex=ex)

  @staticmethod
  def delete(key: str) -> None:
    _instance.delete(key)

