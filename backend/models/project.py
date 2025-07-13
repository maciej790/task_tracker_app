from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .task import Task

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = Field(default=None)
    owner_id: int = Field(foreign_key="user.id")

    owner: Optional["User"] = Relationship(back_populates="projects")
    tasks: List["Task"] = Relationship(back_populates="project")
