import enum

from sqlalchemy import Column, Integer, BigInteger, String, Enum, Text, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class UserRole(str, enum.Enum):
    staff = "staff"
    manager = "manager"


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    overdue = "overdue"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    username = Column(String, nullable=True)
    role = Column(Enum(UserRole), nullable=False)

    tasks = relationship("Task", back_populates="assignee")


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    inn = Column(String, unique=True, nullable=False)
    contact_email = Column(String, nullable=True)

    tasks = relationship("Task", back_populates="client")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=False)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.todo)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    client = relationship("Client", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")