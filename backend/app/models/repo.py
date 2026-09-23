from typing import Optional

from pydantic import BaseModel


class RepoInfo(BaseModel):
    url: str
    name: str
    path: Optional[str] = None
    project_type: Optional[str] = None
    description: Optional[str] = None
