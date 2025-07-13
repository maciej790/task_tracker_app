from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from databse.config import get_session
from services.auth import get_current_user
from services.projects import check_if_project_exists, delete_all_tasks
from schemas.project import Project_in
from models.project import Project
from models.user import User 
from typing import List

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_project(
    project: Project_in,
    db: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    await check_if_project_exists(project, db, user.id)

    project_to_save = Project(owner_id=user.id, **project.model_dump())
    db.add(project_to_save)
    db.commit()
    db.refresh(project_to_save)

    return {"Project has been created successfully!"}

@router.get('/get_all', response_model=List[Project_in], status_code=200)
async def get_all_projects(db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    projects = db.exec(select(Project).where(Project.owner_id == user.id)).all()
    return projects

@router.patch('/update/{id}', status_code=status.HTTP_200_OK)
async def update_project(
    id: int,
    project: Project_in,
    db: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    project_to_update = db.exec(
        select(Project).where(
            (Project.owner_id == user.id) & (Project.id == id)
        )
    ).first()

    if not project_to_update:
        raise HTTPException(status_code=404, detail="Project not found")
    
    await check_if_project_exists(project, db, user.id)

    project_updated_data = project.model_dump(exclude_unset=True)
    project_to_update.sqlmodel_update(project_updated_data)

    db.add(project_to_update)
    db.commit()
    db.refresh(project_to_update)

    return {"Project updated successfully!"}

@router.delete('/delete/{id}')
async def delete_project(id : int, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    project_to_delete = db.exec(
        select(Project).where(
            (Project.owner_id == user.id) & (Project.id == id)
        )
    ).first()

    if not project_to_delete:
        raise HTTPException(status_code=404, detail="Project not found")
    
    await delete_all_tasks(db, id)
    
    db.delete(project_to_delete)
    db.commit()
    
    return {"Project deleted!"}