# 🚀 User Management API — Git Learning Project

A FastAPI project with JWT Authentication, User Management, and Dashboard stats.
Built as a hands-on playground for learning professional **Git workflows**.

---

## 📁 Project Structure

```
git_practice/
├── app/
│   ├── main.py              # FastAPI entry point & Swagger config
│   ├── database.py          # SQLAlchemy DB connection
│   ├── auth/
│   │   ├── router.py        # POST /auth/login
│   │   ├── jwt_handler.py   # Token create & verify
│   │   ├── dependencies.py  # get_current_user (JWT guard)
│   │   └── schemas.py       # LoginRequest, TokenResponse
│   ├── users/
│   │   ├── router.py        # GET/POST/PATCH/DELETE /users
│   │   ├── models.py        # SQLAlchemy User model
│   │   └── schemas.py       # UserCreate, UserOut, UserUpdate
│   └── dashboard/
│       ├── router.py        # GET /dashboard/stats
│       └── schemas.py       # DashboardStats
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Run

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
uvicorn app.main:app --reload

# 4. Open Swagger UI
# http://localhost:8000/docs
```

---

## 🌿 Git Branch Strategy

```
main        ← production
  └── stage ← pre-production / QA
        └── dev ← integration
              ├── feature/user-management
              ├── feature/authentication
              ├── feature/module-management
              └── bug/security-fix
```

---

## 🔐 API Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|--------------|-------------|
| GET | `/` | ❌ | Health check |
| POST | `/auth/login` | ❌ | Login → get JWT token |
| POST | `/users/` | ❌ | Register new user |
| GET | `/users/me` | ✅ | Get my profile |
| GET | `/users/` | ✅ Admin | List all users |
| GET | `/users/{id}` | ✅ | Get user by ID |
| PATCH | `/users/{id}` | ✅ | Update user |
| DELETE | `/users/{id}` | ✅ Admin | Delete user |
| GET | `/dashboard/stats` | ✅ | System stats |
