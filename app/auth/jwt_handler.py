

# Feature: authentication — JWT handler implemented
# Branch: feature/authentication




import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional

# In production, store this in an environment variable — NEVER hardcode it
SECRET_KEY = "your-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a signed JWT token.
    'data' is the payload — we usually put username/user_id here.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Decodes and verifies a JWT token.
    Returns the payload if valid, None if expired or invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None   # Token expired
    except jwt.InvalidTokenError:
        return None   # Token tampered or malformed
