from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import Task, User
from app.models.task import TaskStatus
from app.schemas import TaskCreate, TaskUpdate, PaginatedTasks
from app.schemas.task import Task as TaskSchema


def create_task(db: Session, task_data: TaskCreate, user: User) -> Task:
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        user_id=user.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int, user: User) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


def get_tasks(
    db: Session,
    user: User,
    page: int = 1,
    page_size: int = 10,
    status: Optional[TaskStatus] = None
) -> PaginatedTasks:
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Page must be greater than 0"
        )
    if page_size < 1 or page_size > 100:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Page size must be between 1 and 100"
        )

    query = db.query(Task).filter(Task.user_id == user.id)

    if status:
        query = query.filter(Task.status == status)

    total = query.count()

    tasks = query.order_by(Task.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedTasks(
        total=total,
        page=page,
        page_size=page_size,
        items=[TaskSchema.from_orm(task) for task in tasks]
    )


def update_task(db: Session, task_id: int, task_data: TaskUpdate, user: User) -> Task:
    task = get_task(db, task_id, user)

    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        task.status = task_data.status

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user: User) -> None:
    task = get_task(db, task_id, user)
    db.delete(task)
    db.commit()
