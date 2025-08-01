import pytest
from sqlalchemy import select

from controllers.clients import ClientController
from db.models import Client
from schemas.model import ClientCreate


@pytest.mark.asyncio
async def test_add_client(test_db):

    new_client_data = ClientCreate(
        name="test_client_name",
        inn= "1234567890",
        contact_email="test_email@mail.com")

    controller = ClientController(test_db)
    await controller.add_client(new_client_data)


    async with test_db.session_maker() as session:
        request = select(Client).order_by(Client.id)
        cursor = await session.execute(request)
        client = cursor.scalar_one_or_none()

        assert client.name == "test_client_name"
        assert client.contact_email == "test_email@mail.com"

