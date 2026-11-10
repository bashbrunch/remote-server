from src.core.cache import Cache
from src.models.session import Session

def get_session(
  session_id: str,
  session_key: str,
) -> Session | None:
  if not Cache.get(session_id):
    return None

  session = Session(session_id)

  if not session.auth_check(session_key):
    return None

  return session

def is_available_session(
  session_id: str,
  session_key: str,
) -> bool:
  if not Cache.get(session_id):
    return True

  return Session(session_id).auth_check(session_key)

def create_session(
  session_id: str,
  session_key: str,
) -> Session:
  session = Session(session_id)
  Cache.set(session_id, "1")

  if session_key:
    session.auth_set(session_key)

  return session

def delete_session(
  session_id: str,
  session_key: str,
) -> bool:
  if not Cache.get(session_id):
    return False

  session = Session(session_id)

  if not session.auth_check(session_key):
    return False

  session.destroy()
  Cache.delete(session_id)

  return True

