from fastapi import APIRouter, Depends
from sqlmodel import select
from typing import List

from services.exception import create_exception
from services.tasks import delete_all_tasks, check_if_task_exists

from schemas.task import Task_in, Task_out
from models.project import Project
from models.task import Task

from ..dependencies.common import get_user_and_db

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

# GET all tasks for a project
@router.get('/get_all/{project_id}', response_model=List[Task_out], status_code=200)
async def get_all_tasks_by_project_id(
    project_id: int,
    deps: tuple = Depends(get_user_and_db)
):
    user, db = deps
    tasks = db.exec(
        select(Task).where(
            (Task.project_id == project_id) & (Task.user_id == user.id)
        )
    ).all()
    return tasks

# CREATE a new task
@router.post('/create/{project_id}', status_code=201)
async def create_task_to_project(
    new_task: Task_in,
    project_id: int,
    deps: tuple = Depends(get_user_and_db)
):
    user, db = deps

    project = db.exec(
        select(Project).where(
            (Project.user_id == user.id) & (Project.id == project_id)
        )
    ).first()
    
    if not project:
        create_exception('Project does not exist!', 409)

    if await check_if_task_exists(new_task, project_id, user.id, db):
        create_exception('Task already exists!', 409)

    task_to_create = Task(**new_task.model_dump(), project_id=project_id, user_id=user.id)

    db.add(task_to_create)
    db.commit()
    db.refresh(task_to_create)

    return {'message': 'Task was created!'}

# UPDATE task by id
@router.patch('/update/{project_id}/{task_id}', status_code=200)
async def update_task(
    task: Task_in,
    project_id: int,
    task_id: int,
    deps: tuple = Depends(get_user_and_db)
):
    user, db = deps

    task_to_update = db.exec(
        select(Task).where(
            (Task.id == task_id) & (Task.project_id == project_id) & (Task.user_id == user.id)
        )
    ).first()

    if not task_to_update:
        create_exception("Task does not exist!", 409)

    if await check_if_task_exists(task, project_id, user.id, db):
        create_exception('Task already exists!', 409)

    task_to_update_data = task.model_dump(exclude_unset=True)
    task_to_update.sqlmodel_update(task_to_update_data)

    db.add(task_to_update)
    db.commit()
    db.refresh(task_to_update)

    return {'message': 'Task was updated!'}

# DELETE task by id
@router.delete('/delete/{project_id}/{task_id}', status_code=200)
async def delete_task_from_project(
    project_id: int,
    task_id: int,
    deps: tuple = Depends(get_user_and_db)
):
    user, db = deps

    task_to_delete = db.exec(
        select(Task).where(
            (Task.id == task_id) & (Task.project_id == project_id) & (Task.user_id == user.id)
        )
    ).first()

    if not task_to_delete:
        create_exception("Task does not exist!", 409)

    db.delete(task_to_delete)
    db.commit()

    return {'message': 'Task was deleted!'}

# DELETE all tasks by project_id
@router.delete('/delete_all/{project_id}', status_code=200)
async def delete_all_tasks_from_project(
    project_id: int,
    deps: tuple = Depends(get_user_and_db)
):
    user, db = deps

    project = db.exec(
        select(Project).where(
            (Project.user_id == user.id) & (Project.id == project_id)
        )
    ).first()

    if not project:
        create_exception('Tasks for this project do not exist!', 409)

    await delete_all_tasks(project_id, user.id, db)

    return {'message': 'All tasks were deleted!'}
