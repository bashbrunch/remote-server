from src.models.session import Session

sessions: dict[str, Session] = {}

def get_session(
  session_id: str,
  session_key: str,
) -> Session | None:
  if session_id not in sessions:
    return None

  session = sessions[session_id]

  if session.key and session.key != session_key:
    return None

  return session

def is_available_session(
  session_id: str,
  session_key: str,
) -> bool:
  if session_id not in sessions:
    return True

  session = sessions[session_id]

  if session.key:
    return session.key == session_key

  return True

def create_session(
  session_id: str,
  session_key: str,
) -> Session:
  session = Session()
  sessions[session_id] = session

  if session_key:
    session.key = None

  return session

def delete_session(
  session_id: str,
  session_key: str,
) -> bool:
  if session_id not in sessions:
    return False

  session = sessions[session_id]

  if session.key and session.key != session_key:
    return False

  del sessions[session_id]

  return True

