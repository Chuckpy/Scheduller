from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, String
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
from database.base_class import Base


class TextLine(Base):

    __tablename__ = "text_line"

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

    content = Column(String(500))
    task_id = Column(ForeignKey("task.id"))
    task = relationship("Task", backref="text_lines", foreign_keys=[task_id])

    def __str__(self):
        return f"Text Line #{self.id}"

    def __repr__(self):
        return f"Text Line #{self.id}"

    __mapper_args__ = {
    }
