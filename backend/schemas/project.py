from pydantic import BaseModel
from typing import Optional

class Project_in(BaseModel):
    name: str
    description: Optional[str]