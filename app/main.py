from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.dashboard.router import router as dashboard_router

# ─────────────────────────────────────────────
# Create all DB tables on startup
# ─────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ─────────────────────────────────────────────
# FastAPI app with Swagger metadata
# ─────────────────────────────────────────────
app = FastAPI(
    title="User Management API",
    description="""
## 🔐 JWT-Authenticated REST API

A complete user management system with:

- **Authentication** — Login with username & password → receive JWT token
- **User Management** — Create, read, update, delete users
- **Dashboard** — System statistics (protected)

### How to use Swagger UI:
1. Use `POST /auth/login` with your credentials
2. Copy the `access_token` from the response
3. Click the **🔒 Authorize** button at the top right
4. Enter: `Bearer <your_token>` and click Authorize
5. All protected endpoints are now unlocked!
    """,
    version="1.0.0",
    contact={"name": "Priyanshi", "email": "priyanshi@example.com"},
    license_info={"name": "MIT"},
)

# ─────────────────────────────────────────────
# CORS — allows frontend/Swagger to call API
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Register all routers
# ─────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(dashboard_router)


# ─────────────────────────────────────────────
# Health check (no auth required)
# ─────────────────────────────────────────────
@app.get("/", tags=["Health"], summary="Health check")
def root():
    return {"status": "ok", "message": "User Management API is running 🚀"}
