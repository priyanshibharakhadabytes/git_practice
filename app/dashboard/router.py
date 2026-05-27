
# New feature being developed — NOT ready for production yet



from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.users.models import User
from app.auth.dependencies import get_current_user
from app.dashboard.schemas import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "/stats",
    response_model=DashboardStats,
    summary="Get dashboard statistics",
    description="""
Returns a summary of system-wide user statistics.

- `total_users`: How many users are registered
- `active_users`: Users with `is_active = true`
- `admin_count`: How many admin accounts exist
- `newest_user`: Username of the most recently registered user
- `your_last_login`: Your own last login timestamp
- `your_role`: Your current role (user / admin)

**Requires JWT Bearer token.**
    """,
)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    admin_count = db.query(User).filter(User.role == "admin").count()

    newest = (
        db.query(User)
        .order_by(User.created_at.desc())
        .first()
    )

    return DashboardStats(
        total_users=total_users,
        active_users=active_users,
        admin_count=admin_count,
        newest_user=newest.username if newest else None,
        your_last_login=current_user.last_login,
        your_role=current_user.role,
    )
