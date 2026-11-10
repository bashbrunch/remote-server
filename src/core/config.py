from os import getenv

class Config:
  REDIS_URL = getenv("REDIS_URL", "")

