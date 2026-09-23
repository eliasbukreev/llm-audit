from pydantic import BaseModel
from typing import Optional


class RepoInfo(BaseModel):
    url: str
    name: str
    path: Optional[str] = None
    project_type: Optional[str] = None
    description: Optional[str] = None
