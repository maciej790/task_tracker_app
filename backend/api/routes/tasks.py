from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from databse.config import get_session
from services.auth import get_current_user
from schemas.project import Project_in
from models.project import Project
from schemas.task import Task_in, Task_out
from models.task import Task
from models.user import User 
from typing import List
from services.projects import check_if_project_exists
from services.exception import create_exception
from services.tasks import delete_all_tasks, check_if_task_exists
from services.exception import create_exception
from services.tasks import delete_all_tasks

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

#get all tasks
@router.get('/get_all/{project_id}', response_model=List[Task_out], status_code=200)
async def get_all_tasks_by_project_id(project_id : int, db : Session = Depends(get_session), user : User = Depends(get_current_user)):
    tasks = db.exec(select(Task).where(Task.project_id == project_id)).all()
    return tasks

#create new task
@router.post('/create/{project_id}', status_code=201)
async def create_task_to_project(new_task : Task_in, project_id : int, db : Session = Depends(get_session), user : User = Depends(get_current_user)):
    project = db.exec(
        select(Project).where(
            (Project.user_id == user.id) & (Project.id == project_id)
        )
    ).first()
    
    if not project:
        create_exception('Project does not exsist!', 409)
    if await check_if_task_exists(new_task, project_id, user.id, db):
        create_exception('Task already exists!', 409) 
        
    task_to_create = Task(**new_task.model_dump(), project_id=project_id, user_id=user.id)
        
    db.add(task_to_create)
    db.commit()
    db.refresh(task_to_create)
    
    return {'task was created!'}

#update task by id
@router.patch('/update/{project_id}/{task_id}', status_code=200)
async def update_task(task : Task_in, project_id : int, task_id : int, db : Session = Depends(get_session), user : User = Depends(get_current_user)):    
    task_to_update = db.exec(
        select(Task).where(
            (Task.id == task_id) & (Task.project_id == project_id) & (Task.user_id == user.id)
        )
    ).first()
    
    if not task_to_update:
        create_exception("Task does not exsist!", 409)
        
    if await check_if_task_exists(task, project_id, user.id, db):
        create_exception('Task already exists!', 409)
        
    task_to_update_data = task.model_dump(exclude_unset=True)
    task_to_update.sqlmodel_update(task_to_update_data)
    
    
    db.add(task_to_update)
    db.commit()
    db.refresh(task_to_update)
    
    return {'task was updated!'}

#delete task by id
@router.delete('/delete/{project_id}/{task_id}', status_code=201)
async def delete_task_from_project(task : Task_in, project_id : int, task_id : int, db : Session = Depends(get_session), user : User = Depends(get_current_user)):
    task_to_delete = db.exec(
        select(Task).where(
            (Task.id == task_id) & (Task.project_id == project_id) & (Task.user_id == user.id)
        )
    ).first()
    
    if not task_to_delete:
        create_exception("Task does not exsist!", 409)

    db.delete(task_to_delete)
    db.commit()
    
    return {'task was deleted!'}

#delete all tasks by project id
@router.delete('/delete/{project_id}', status_code=201)
async def delete_all_tasks_from_project(project_id : int, db : Session = Depends(get_session), user : User = Depends(get_current_user)):
    project = db.exec(
        select(Project).where(
            (Project.user_id == user.id) & (Project.id == project_id)
        )
    ).first()
    
    if not project:
        create_exception('tasks for this project do not exist!', 409)
    
    await delete_all_tasks(project_id, user.id, db)
    
    return {'all tasks were deleted!'}
