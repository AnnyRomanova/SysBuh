from datetime import date

import pytest

from controllers.tasks import TaskController
from schemas.model import TaskOut
from src.db.models import Task, Client, User, TaskStatus, UserRole


@pytest.mark.asyncio
async def test_get_tasks_list(test_db):
    async with test_db.session_maker() as session:
        client = Client(
            name="Test Client",
            inn="1234567890",
            contact_email="client@example.com"
        )
        user = User(
            telegram_id=123456789,
            full_name="Test User",
            username="testuser",
            role=UserRole.staff
        )
        session.add_all([client, user])
        await session.flush()

        task = Task(
            title="Test Task",
            description="Test Description",
            due_date=date(2025, 1, 1),
            status=TaskStatus.todo,
            client_id=client.id,
            executor_id=user.id
        )
        session.add(task)
        await session.commit()

    controller = TaskController(test_db)
    tasks = await controller.get_tasks_list()

    assert len(tasks) == 1
    task_out = tasks[0]
    assert isinstance(task_out, TaskOut)
    assert task_out.title == "Test Task"
    assert task_out.client.name == "Test Client"
    assert task_out.executor.full_name == "Test User"
