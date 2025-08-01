import logging

from sqlalchemy import select

from db.models import Client
from db.session import DatabaseConnector
from schemas.model import ClientOut, ClientCreate
from src.exceptions import ClientNotFoundError

logger = logging.getLogger(__name__)


class ClientController:

    def __init__(self, db: DatabaseConnector):
        self.db = db

    async def get_clients_list(self) -> list[ClientOut]:
        logger.info("Clients list requested")
        async with self.db.session_maker() as session:
            request = select(Client).order_by(Client.id)
            cursor = await session.execute(request)
            clients = cursor.scalars().all()

            clients_list = []
            for client in clients:
                clients_list.append(ClientOut(
                        id=client.id,
                        name=client.name,
                        inn=client.inn,
                        contact_email=client.contact_email,
                    )
                )

            return clients_list



    async def add_client(self, client_data: ClientCreate) -> None:
        logger.info("Request to add new client to db")
        async with self.db.session_maker() as session:
            new_client = Client(**client_data.model_dump())
            session.add(new_client)
            await session.commit()


    async def delete_client(self, client_inn: str) -> None:
        logger.info("Request to delete post")
        async with self.db.session_maker() as session:
            stmt = select(Client).where(Client.inn == client_inn)
            cursor = await session.execute(stmt)
            existing_client = cursor.scalar_one_or_none()

            if not existing_client:
                raise ClientNotFoundError("Клиент не найден")

            await session.delete(existing_client)
            await session.commit()
        logger.info("Client deleted")


client_controller: ClientController | None = None


def get_client_controller() -> ClientController:
    assert client_controller is not None, "ClientController not initialized"
    return client_controller