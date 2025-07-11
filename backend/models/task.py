from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import enum

if TYPE_CHECKING:
    from .project import Project

class TaskStatus(str, enum.Enum):
    inprogress = "inprogress"
    done = "done"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.inprogress)
    deadline: Optional[datetime] = Field(default=None)
    priority: int = Field(default=3)

    project_id: int = Field(foreign_key="project.id")
    project: Optional["Project"] = Relationship(back_populates="tasks")
