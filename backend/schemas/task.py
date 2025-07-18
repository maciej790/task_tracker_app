from pydantic import BaseModel
from typing import Optional
import enum
from datetime import datetime

class TaskStatus(str, enum.Enum):
    inprogress = "inprogress"
    done = "done"

class Task_in(BaseModel):
    title: str
    description: Optional[str]
    status: TaskStatus
    deadline: Optional[datetime]
    priority: int
