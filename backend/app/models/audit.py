from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AuditStep(BaseModel):
    id: str
    name: str
    status: str = "pending"
    result_path: Optional[str] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None


class AuditSession(BaseModel):
    id: str
    repo_url: str
    repo_name: Optional[str] = None
    repo_path: Optional[str] = None
    results_dir: Optional[str] = None
    status: str = "idle"
    steps: list[AuditStep] = []
    error_msg: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
