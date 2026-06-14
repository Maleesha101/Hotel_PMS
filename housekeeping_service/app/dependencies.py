"""FastAPI dependencies for authentication and role based access control.

The service uses JWT RS256 tokens. The public key is supplied via the
environment (``settings.JWT_PUBLIC_KEY``). Tokens are expected to contain a
``sub`` claim (user id) and a ``roles`` claim – a list of role strings.
"""

from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel, ValidationError, Field, model_validator

from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")  # token endpoint is external

class TokenPayload(BaseModel):
    sub: str  # user identifier
    roles: List[str] = []
    exp: int | None = None

    @model_validator(mode="before")
    @classmethod
    def map_role_to_roles(cls, data: dict) -> dict:
        # Support tokens that use 'role' (string) instead of 'roles' (list)
        if "role" in data and not data.get("roles"):
            role = data["role"]
            data["roles"] = [role] if isinstance(role, str) else role
        return data

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
        if not settings.JWT_PUBLIC_KEY:
            raise ValueError("JWT_PUBLIC_KEY is not configured in environment")
            
        # Fix: Disable audience verification or provide the expected audience
        payload = jwt.decode(
            token, 
            settings.JWT_PUBLIC_KEY, 
            algorithms=["RS256"],
            options={"verify_aud": False} 
        )
        token_data = TokenPayload(**payload)
        return token_data
    except (JWTError, ValidationError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(exc)}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(exc)}"
        ) from exc

def require_roles(*allowed_roles: str):
    """Dependency factory that enforces role based access.

    ``allowed_roles`` is a list of role names that are permitted to access the
    endpoint. If the current user's ``roles`` claim does not intersect with this
    list, a 403 response is returned.
    """
    def role_checker(user: TokenPayload = Depends(get_current_user)):
        # Normalize both user roles and allowed roles to uppercase for a case-insensitive check
        user_roles_set = {r.upper() for r in user.roles}
        allowed_roles_set = {r.upper() for r in allowed_roles}
        
        if not user_roles_set.intersection(allowed_roles_set):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role privileges",
            )
        return user
    return role_checker
