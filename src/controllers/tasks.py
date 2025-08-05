import logging

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.models import Task, User
from db.session import DatabaseConnector
from schemas.model import TaskOut

logger = logging.getLogger(__name__)


class TaskController:

    def __init__(self, db: DatabaseConnector):
        self.db = db

    async def get_tasks_list(self) -> list[TaskOut]:
        logger.info("Clients list requested")
        async with self.db.session_maker() as session:
            stmt = (
                select(Task)
                .options(
            selectinload(Task.client),
                    selectinload(Task.executor)
                )
                .order_by(Task.id)
            )
            result = await session.execute(stmt)
            tasks = result.scalars().all()

            tasks_list = []
            for task in tasks:
                tasks_list.append(TaskOut(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    due_date=task.due_date,
                    status=task.status,
                    client=task.client,
                    executor=task.executor
                    )
                )

            return tasks_list

    async def get_tasks_for_user(self, telegram_id: int) -> list[TaskOut]:
        logger.info(f"Task list requested for user {telegram_id}")
        async with self.db.session_maker() as session:
            stmt = (
                select(Task)
                .join(Task.executor)
                .options(
                    selectinload(Task.client),
                    selectinload(Task.executor),
                )
                .where(User.telegram_id == telegram_id)
            )

            result = await session.execute(stmt)
            tasks = result.scalars().all()

            tasks_list = []
            for task in tasks:
                tasks_list.append(TaskOut(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    due_date=task.due_date,
                    status=task.status,
                    client=task.client,
                    executor=task.executor
                )
                )
            return tasks_list


task_controller: TaskController | None = None


def get_task_controller() -> TaskController:
    assert task_controller is not None, "TaskController not initialized"
    return task_controller