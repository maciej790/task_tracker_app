from fastapi import Depends, HTTPException, status
from databse.config import get_session
from sqlmodel import Session, select, delete
from schemas.task import Task_in
from models.task import Task
from models.task import Task
from models.project import Project

async def check_if_project_exists(id : int, user_id: int, db: Session):
    existing_project = db.exec(
        select(Project).where(
            (Project.id == id) & (Project.owner_id == user_id)
        )
    ).first()

    if not existing_project:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project does not exsist!",
        )
    return True

async def check_if_task_exists(task, db: Session, task_id: int):
    existing_project = db.exec(
        select(Task).where(
            (Task.title == task.title) & (Task.project_id == task_id)
        )
    ).first()

    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task already exists!",
        )
    return True