from database.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from core.apps.tasks.models import Task
from core.apps.cash_flow.models import CashFlow
from core.apps.chat.models import Message, Room


class User(BaseModel):
    
    __tablename__ = "users"

    username = Column(String(255), unique=True, nullable=False)

    first_name = Column(String(255))

    last_name = Column(String(255))

    full_name = Column(String(255))

    hashed_password = Column(String(255))

    email = Column(String(255), unique=True, nullable=False)

    group_id = Column(ForeignKey("auth_group.id"), nullable=True)

    group = relationship("Group", backref="users", foreign_keys=[group_id])

    tasks = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete",
        foreign_keys=[Task.user_id],
    )

    cash_flows = relationship(
        "CashFlow",
        back_populates="user",
        cascade="all, delete",
        foreign_keys=[CashFlow.user_id],
    )

    messages = relationship(
        "Message",
        back_populates="user",
        cascade="all, delete",
        foreign_keys=[Message.user_id],
    )

    rooms = relationship(
        "Room",
        back_populates="user",
        cascade="all, delete",
        foreign_keys=[Room.user_id],
    )

    def __str__(self):
        return f"#{self.id} - {self.first_name}"

    def __repr__(self):
        return f"#{self.id} - {self.first_name}"

    __mapper_args__ = {}
