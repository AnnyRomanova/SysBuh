import pytest
from src.controllers.clients import ClientController
from src.db.models import Client


@pytest.mark.asyncio
async def test_get_clients_list(test_db):

    async with test_db.session_maker() as session:
        session.add_all([
            Client(name="Client 1", inn="1234567890", contact_email="client1@test.com"),
            Client(name="Client 2", inn="9876543210", contact_email="client2@test.com"),
        ])
        await session.commit()

    controller = ClientController(test_db)

    result = await controller.get_clients_list()

    assert len(result) == 2
    assert result[0].name == "Client 1"
    assert result[1].inn == 9876543210
