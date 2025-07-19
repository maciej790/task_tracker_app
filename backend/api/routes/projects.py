from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import List

from services.projects import check_if_project_exists
from services.exception import create_exception
from services.tasks import delete_all_tasks

from schemas.project import Project_in
from models.project import Project

from ..dependencies.common import get_user_and_db


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)

# GET all projects
@router.get('/get_all', response_model=List[Project], status_code=200)
async def get_all_projects(deps: tuple = Depends(get_user_and_db)):
    user, db = deps
    projects = db.exec(
        select(Project).where(Project.user_id == user.id)
    ).all()
    return projects

# CREATE new project
@router.post('/create', status_code=201)
async def create_new_project(
    new_project: Project_in,
    deps: tuple = Depends(get_user_and_db)
):
    user, db = deps

    if await check_if_project_exists(new_project.name, user.id, db):
        create_exception("Project already exists!", 409)

    project_to_save = Project(user_id=user.id, **new_project.model_dump())
    
    db.add(project_to_save)
    db.commit()
    db.refresh(project_to_save)

    return {'message': 'Project created!'}

# UPDATE project
@router.patch('/update/{project_id}', status_code=200)
async def update_project(
    project_id: int,
    updated_project: Project_in,
    deps: tuple = Depends(get_user_and_db)
):
    user, db = deps

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

    return {"message": "Project updated successfully!"}

# DELETE project
@router.delete('/delete/{project_id}', status_code=200)
async def delete_project(
    project_id: int,
    deps: tuple = Depends(get_user_and_db)
):
    user, db = deps

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

    return {"message": "Project deleted!"}
