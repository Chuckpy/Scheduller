from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from core.apps.tasks.models import Task
from core.apps.cash_flow.models import CashFlow

from database.base_class import Base



class User(Base):

    __tablename__ = "users"

    id = Column(
        UUIDType(binary=False),
        primary_key=True,
        default=uuid4()
    )

    is_active = Column(Boolean, default=True)

    created = Column(
        DateTime(timezone=True),
        server_default=func.now()
        )

    updated = Column(
        DateTime(timezone=True), 
        onupdate=func.now()
        )

    username = Column(
        String(255), 
        unique=True, 
        nullable=False
        )

    first_name = Column(String(255))

    last_name = Column(String(255))

    full_name = Column(String(255))

    hashed_password = Column(String(255))

    email = Column(
        String(255), 
        unique=True, 
        nullable=False
        )

    group_id = Column(
        ForeignKey("auth_group.id"),
        nullable=True
        )

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

    def __str__(self):
        return f"#{self.id} - {self.first_name}"

    def __repr__(self):
        return f"#{self.id} - {self.first_name}"

    __mapper_args__ = {
    }
