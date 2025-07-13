from fastapi import Depends, HTTPException, status
from databse.config import get_session
from sqlmodel import Session, select, delete
from schemas.project import Project_in
from models.project import Project
from models.task import Task

async def check_if_project_exists(project, db: Session, user_id: int):
    existing_project = db.exec(
        select(Project).where(
            (Project.name == project.name) & (Project.owner_id == user_id)
        )
    ).first()

    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project already exists!",
        )
    return True

#propably this function should by transported to services/task !
async def delete_all_tasks(db: Session, project_id: int):
    db.exec(
        delete(Task).where(Task.project_id == project_id)
    )
    db.commit()