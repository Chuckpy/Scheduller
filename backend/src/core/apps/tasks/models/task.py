from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
from database.base_class import Base


class Task(Base):

    __tablename__ = "task"

    id = Column(
        UUIDType(binary=False),
        primary_key=True,
        default=uuid4()
    )

    created = Column(
        DateTime(timezone=True),
        server_default=func.now()
        )

    updated = Column(
        DateTime(timezone=True), 
        onupdate=func.now()
        )

    is_active = Column(Boolean, default=True)

    user_id = Column(
        ForeignKey("users.id"),
        nullable=False,
    )

    user = relationship("User", back_populates="tasks", foreign_keys=[user_id])

    deadline = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    description = Column(
        String(255),
        nullable=False,
    )

    task_group_id = Column(ForeignKey("task_group.id"), nullable=True)

    task_group = relationship(
        "TaskGroup", backref="tasks", foreign_keys=[task_group_id]
    )

    def __str__(self):
        return f"Task #{self.id}"

    def __repr__(self):
        return f"Task #{self.id}"

    __mapper_args__ = {}

