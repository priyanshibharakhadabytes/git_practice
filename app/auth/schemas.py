from pydantic import BaseModel


# What the client sends to login
class LoginRequest(BaseModel):
    username: str
    password: str


# What we return after a successful login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800   # seconds (30 minutes)
