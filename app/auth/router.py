from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

import bcrypt

from app.database import get_db
from app.users.models import User
from app.auth.jwt_handler import create_access_token
from app.auth.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login with username and password",
    description="""
Authenticate a user using their **username** and **password**.

On success, returns a **JWT Bearer token** that must be included in the
`Authorization` header for all protected endpoints:

```
Authorization: Bearer <your_token_here>
```

The token expires in **30 minutes**.
    """,
)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    # Step 1: Find user by username
    user = db.query(User).filter(User.username == payload.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Step 2: Verify password against stored hash
    password_valid = bcrypt.checkpw(
        payload.password.encode("utf-8"),
        user.hashed_password.encode("utf-8")
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Step 3: Check account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been disabled. Contact admin.",
        )

    # Step 4: Update last_login timestamp
    user.last_login = datetime.now(timezone.utc)
    db.commit()

    # Step 5: Create JWT token — "sub" (subject) holds the username
    token = create_access_token(data={"sub": user.username, "role": user.role})

    return TokenResponse(access_token=token)
