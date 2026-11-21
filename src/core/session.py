from src.core.cache import Cache
from src.models.session import Session

async def get_session(
  session_id: str,
  session_key: str,
) -> Session | None:
  if not await Cache.get(session_id):
    return None

  session = Session(session_id)

  if not await session.auth_check(session_key):
    return None

  return session

async def is_available_session(
  session_id: str,
  session_key: str,
) -> bool:
  if not await Cache.get(session_id):
    return True

  session = Session(session_id)
  valid = await session.auth_check(session_key)

  return valid

async def create_session(
  session_id: str,
  session_key: str,
) -> Session:
  session = Session(session_id)
  await Cache.set(session_id, "1")

  if session_key:
    await session.auth_set(session_key)

  return session

async def delete_session(
  session_id: str,
  session_key: str,
) -> bool:
  if not await Cache.get(session_id):
    return False

  session = Session(session_id)

  if not await session.auth_check(session_key):
    return False

  await session.destroy()
  await Cache.delete(session_id)

  return True

