import pytest
from sqlalchemy import select

from controllers.clients import ClientController
from db.models import Client
from src.exceptions import ClientNotFoundError


@pytest.mark.asyncio
async def test_delete_client_success(test_db):

    async with test_db.session_maker() as session:
        session.add_all([
            Client(name="Client 1", inn="1234567890", contact_email="client1@test.com"),
            Client(name="Client 2", inn="9876543210", contact_email="client2@test.com"),
            Client(name="Client 3", inn="5432167890", contact_email="client3@test.com")
        ])
        await session.commit()

        client_to_delete = await session.scalar(
            select(Client).where(Client.inn == "1234567890")
        )

    controller = ClientController(test_db)
    await controller.delete_client(client_to_delete.inn)

    async with test_db.session_maker() as session:
        clients = await session.scalars(select(Client).order_by(Client.id))
        clients = list(clients)

        assert len(clients) == 2
        assert clients[0].name == "Client 2"


@pytest.mark.asyncio
async def test_delete_client_error(test_db):
    async with test_db.session_maker() as session:
        session.add_all([
            Client(name="Client 1", inn="1234567890", contact_email="client1@test.com"),
            Client(name="Client 2", inn="9876543210", contact_email="client2@test.com"),
            Client(name="Client 3", inn="5432167890", contact_email="client3@test.com")
        ])
        await session.commit()

    controller = ClientController(test_db)

    with pytest.raises(ClientNotFoundError):
        await controller.delete_client("1111111111")

