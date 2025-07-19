from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import enum

if TYPE_CHECKING:
    from .user import User
    from .project import Project

class TaskStatus(str, enum.Enum):
    inprogress = "inprogress"
    done = "done"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    status: TaskStatus
    color: int
    project_id: int = Field(foreign_key="projects.id")
    user_id: int = Field(foreign_key="users.id")
    deadline: Optional[datetime] = Field(default=None)  

    project: Optional["Project"] = Relationship(back_populates="tasks")
    user: Optional["User"] = Relationship(back_populates="tasks")