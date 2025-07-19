from fastapi import Depends, HTTPException, status
from databse.config import get_session
from sqlmodel import Session, select, delete
from schemas.project import Project_in
from models.project import Project
from models.task import Task

async def delete_all_tasks(project_id: int, user_id: int,  db: Session):
    db.exec(
        delete(Task).where((Task.project_id == project_id) & Task.user_id == user_id)
    )
    db.commit()
    
async def check_if_task_exists(task, project_id: int, user_id: int, db: Session):
    existing_task = db.exec(
        select(Task).where(
            (Task.title == task.title) & (Task.project_id == project_id) & (Task.user_id == user_id)
        )
    ).first()

    if existing_task:
        return True
        
    return False