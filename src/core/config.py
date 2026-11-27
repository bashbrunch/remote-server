from os import getenv

def read(fname: str) -> str:
  with open(fname, "r") as f:
    return f.read().strip()

class Config:
  REDIS_URL = getenv("REDIS_URL", "")
  VERSION = read("VERSION")

