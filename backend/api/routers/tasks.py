from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from databse.config import get_session
from services.auth import get_current_user
from models.task import Task
from models.user import User 
from schemas.task import Task_in
from typing import List
from services.tasks import check_if_project_exists, check_if_task_exists

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get('/getAll/{project_id}', response_model=List[Task_in], status_code=200)
async def get_all_tasks_by_project_id(id : int, db : Session = Depends(get_session), user : User = Depends(get_current_user)):
    tasks = db.exec(select(Task).where(Task.project_id == id)).all()
    return tasks

@router.post('/create/{project_id}', status_code=201)
async def create_task_to_project(task : Task_in, id : int, db : Session = Depends(get_session), user : User = Depends(get_current_user)):
    await check_if_project_exists(id, user.id, db)
    await check_if_task_exists(task, db, id)
    
    task_to_create = Task(**task.model_dump(), project_id=id)
    
    db.add(task_to_create)
    db.commit()
    db.refresh(task_to_create)
    
    return {'task was created!'}

@router.patch('/update/{project_id}/{task_id}', status_code=200)
async def create_task_to_project(task : Task_in, project_id : int, task_id : int, db : Session = Depends(get_session), user : User = Depends(get_current_user)):
    await check_if_project_exists(project_id, user.id, db)
    
    task_to_update = db.exec(
        select(Task).where(
            (Task.id == task_id)
        )
    ).first()
    
    if not task_to_update:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task does not exsist!",
        )
        
    task_to_update_data = task.model_dump(exclude_unset=True)
    task_to_update.sqlmodel_update(task_to_update_data)
    
    db.add(task_to_update)
    db.commit()
    db.refresh(task_to_update)
    
    return {'task was updated!'}

@router.delete('/delete/{project_id}/{task_id}', status_code=201)
async def delete_task_from_project(task : Task_in, project_id : int, task_id : int, db : Session = Depends(get_session), user : User = Depends(get_current_user)):
    await check_if_project_exists(project_id, user.id, db)
    await check_if_task_exists(task, db, task_id)
    
    task_to_delete = db.get(Task, task_id)
    
    db.delete(task_to_delete)
    db.commit()
    
    return {'task was deleted!'}