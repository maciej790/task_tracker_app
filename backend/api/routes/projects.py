from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from databse.config import get_session
from services.auth import get_current_user
from schemas.project import Project_in
from models.project import Project
from models.user import User 
from typing import List
from services.projects import check_if_project_exists
from services.exception import create_exception
from services.tasks import delete_all_tasks

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

#get all projects
@router.get('/get_all', status_code=200, response_model=List[Project])
async def get_all_projects(user = Depends(get_current_user), db : Session = Depends(get_session)):
    projects = db.exec(select(Project)).all()
    return projects

#create new project
@router.post('/create', status_code=201)
async def create_new_project(new_project : Project_in, user = Depends(get_current_user), db : Session = Depends(get_session)):
    if await check_if_project_exists(new_project.name, user.id, db):
        create_exception("Project already exists!", 409)
    
    project_to_save = Project(user_id=user.id, **new_project.model_dump())
    
    db.add(project_to_save)
    db.commit()
    db.refresh(project_to_save)
    
    return {'created!'}

#update project
@router.patch('/update/{id}', status_code=200)
async def update_project(
    project_id: int,
    updated_project: Project_in,
    db: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    project_to_update = db.exec(
        select(Project).where(
            (Project.user_id == user.id) & (Project.id == project_id)
        )
    ).first()

    if not project_to_update:
        create_exception("Project not found", 404)
    
    if await check_if_project_exists(updated_project.name, user.id, db):
        create_exception("Project already exists!", 409)
    
    project_updated_data = updated_project.model_dump(exclude_unset=True)
    project_to_update.sqlmodel_update(project_updated_data)
    
    db.add(project_to_update)
    db.commit()
    db.refresh(project_to_update)

    return {"Project updated successfully!"}

#delete project
@router.delete('/delete/{id}')
async def delete_project(project_id : int, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    project_to_delete = db.exec(
        select(Project).where(
            (Project.user_id == user.id) & (Project.id == project_id)
        )
    ).first()

    if not project_to_delete:
        create_exception("Project not found", 404)
    
    await delete_all_tasks(project_id, user.id, db)
    
    db.delete(project_to_delete)
    db.commit()
    
    return {"Project deleted!"}