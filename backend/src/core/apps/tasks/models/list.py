from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
from database.base_class import Base


class List(Base):

    __tablename__ = "list"

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

    task_id = Column(
        ForeignKey("task.id"),
        nullable=False,
    )
    task = relationship("Task", backref="lists", foreign_keys=[task_id])

    def __str__(self):
        return f"List #{self.id}"

    def __repr__(self):
        return f"List #{self.id}"

    __mapper_args__ = {
    }
