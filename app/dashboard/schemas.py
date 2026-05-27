from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DashboardStats(BaseModel):
    total_users: int
    active_users: int
    admin_count: int
    newest_user: Optional[str] = None
    your_last_login: Optional[datetime] = None
    your_role: str
