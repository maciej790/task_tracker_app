from fastapi import HTTPException, status
from sqlmodel import Session, select
from models.project import Project

async def check_if_project_exists(project_name : str, user_id : id, db : Session):
    project = db.exec(
        select(Project).where(
            (Project.name == project_name) & (Project.user_id == user_id)
        )
    ).first()
    
    if project:
        return True
    return False