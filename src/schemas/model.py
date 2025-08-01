from datetime import datetime

from pydantic import BaseModel

from db.models import UserRole, TaskStatus


class ClientCreate(BaseModel):
    name: str
    inn: str
    contact_email: str

    model_config = {
        "from_attributes": True
    }


class ClientOut(ClientCreate):
    id: int

    model_config = {
        "from_attributes": True
    }


class User(BaseModel):
    id: int
    telegram_id: int
    full_name: str
    username: str
    role: UserRole

    model_config = {
        "from_attributes": True
    }


class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: datetime
    client_id: int
    executor: User

    model_config = {
        "from_attributes": True
    }


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    status: TaskStatus
    client: ClientOut
    executor: User

    model_config = {
        "from_attributes": True
    }






