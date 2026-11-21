from redis.asyncio import Redis

from src.core.config import Config

_instance: Redis = Redis.from_url(Config.REDIS_URL)

class Cache:
  @staticmethod
  async def get(key: str, default: str = "") -> str:
    raw = await _instance.get(key)

    if raw is None:
      return default

    data: str = ""

    if isinstance(raw, bytes):
      data = raw.decode()
    else:
      data = str(raw)

    return data

  @staticmethod
  async def set(key: str, value: str, ex: int | None = None) -> None:
    await _instance.set(key, value, ex=ex)

  @staticmethod
  async def delete(key: str) -> None:
    await _instance.delete(key)

