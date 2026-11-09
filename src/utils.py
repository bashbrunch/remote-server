from random import randint

def generate_key() -> str:
  return hex(randint(1 << 63, 1 << 64))[2:]

