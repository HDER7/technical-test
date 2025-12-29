"""
Script to initialize database with initial user and optional seed data.
"""
from app.db.session import SessionLocal
from app.models import User, Task
from app.models.task import TaskStatus
from app.core.security import get_password_hash
from app.core.config import settings


def init_db():
    db = SessionLocal()
    try:
        # Check if initial user already exists
        existing_user = db.query(User).filter(User.email == settings.INITIAL_USER_EMAIL).first()

        if existing_user:
            print(f"Initial user already exists: {settings.INITIAL_USER_EMAIL}")
            return

        # Create initial user
        initial_user = User(
            email=settings.INITIAL_USER_EMAIL,
            hashed_password=get_password_hash(settings.INITIAL_USER_PASSWORD),
            is_active=True
        )
        db.add(initial_user)
        db.commit()
        db.refresh(initial_user)

        print(f"Initial user created successfully!")
        print(f"Email: {settings.INITIAL_USER_EMAIL}")
        print(f"Password: {settings.INITIAL_USER_PASSWORD}")

        # Optional: Create some seed tasks
        seed_tasks = [
            Task(
                title="Setup development environment",
                description="Install all required dependencies and setup the project",
                status=TaskStatus.DONE,
                user_id=initial_user.id
            ),
            Task(
                title="Implement authentication",
                description="Create JWT-based authentication system",
                status=TaskStatus.DONE,
                user_id=initial_user.id
            ),
            Task(
                title="Create task CRUD endpoints",
                description="Implement create, read, update, delete operations for tasks",
                status=TaskStatus.IN_PROGRESS,
                user_id=initial_user.id
            ),
            Task(
                title="Add pagination to task listing",
                description="Implement pagination for the tasks endpoint",
                status=TaskStatus.PENDING,
                user_id=initial_user.id
            ),
            Task(
                title="Write documentation",
                description="Create comprehensive README with setup instructions",
                status=TaskStatus.PENDING,
                user_id=initial_user.id
            ),
        ]

        for task in seed_tasks:
            db.add(task)

        db.commit()
        print(f"Created {len(seed_tasks)} seed tasks")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Done!")
