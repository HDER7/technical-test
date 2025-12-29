from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models import User
from app.models.task import TaskStatus
from app.schemas import TaskCreate, TaskUpdate, PaginatedTasks
from app.schemas.task import Task
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new task.

    - **title**: Task title (required)
    - **description**: Task description (optional)
    - **status**: Task status (pending, in_progress, done) - defaults to pending
    """
    return task_service.create_task(db, task_data, current_user)


@router.get("", response_model=PaginatedTasks)
def get_tasks(
    page: int = 1,
    page_size: int = 10,
    status: Optional[TaskStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get paginated list of tasks.

    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 10, max: 100)
    - **status**: Filter by status (optional)
    """
    return task_service.get_tasks(db, current_user, page, page_size, status)


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific task by ID.
    """
    return task_service.get_task(db, task_id, current_user)


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a task.

    - **title**: New task title (optional)
    - **description**: New task description (optional)
    - **status**: New task status (optional)
    """
    return task_service.update_task(db, task_id, task_data, current_user)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a task.
    """
    task_service.delete_task(db, task_id, current_user)
    return None
