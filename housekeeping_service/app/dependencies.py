"""FastAPI dependencies for authentication and role based access control.

The service uses JWT RS256 tokens. The public key is supplied via the
environment (``settings.JWT_PUBLIC_KEY``). Tokens are expected to contain a
``sub`` claim (user id) and a ``roles`` claim – a list of role strings.
"""

from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel, ValidationError

from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")  # token endpoint is external

class TokenPayload(BaseModel):
    sub: str  # user identifier
    roles: List[str] = []
    exp: int | None = None

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """Validate a JWT and return its payload.

    Raises ``HTTPException`` 401 if the token is missing, malformed, expired,
    or cannot be verified with the configured public key.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
        )
    try:
        payload = jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=["RS256"])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        ) from exc
    return token_data

def require_roles(*allowed_roles: str):
    """Dependency factory that enforces role based access.

    ``allowed_roles`` is a list of role names that are permitted to access the
    endpoint. If the current user's ``roles`` claim does not intersect with this
    list, a 403 response is returned.
    """
    def role_checker(user: TokenPayload = Depends(get_current_user)):
        if not set(user.roles).intersection(allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role privileges",
            )
        return user
    return role_checker
