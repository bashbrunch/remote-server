from fastapi import Depends, HTTPException, Request
from fastapi.security import APIKeyHeader

from src.core.session import get_session

security = APIKeyHeader(
  name="Authorization",
  auto_error=False,
)

async def session_authenticate(
  session_id: str,
  request: Request,
  session_key: str = Depends(security),
):
  session = get_session(session_id, session_key)

  if not session:
    raise HTTPException(
      status_code=403,
      detail="access denied",
    )

  request.state.session = session

