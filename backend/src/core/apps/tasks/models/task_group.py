from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy_utils import UUIDType
from sqlalchemy.sql import func
from uuid import uuid4
from database.base_class import Base


class TaskGroup(Base):

    __tablename__ = "task_group"

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

    title = Column(String(255))

    def __str__(self):
        return f"Task Group #{self.id}"

    def __repr__(self):
        return f"Task Group #{self.id}"

    __mapper_args__ = {
    }
