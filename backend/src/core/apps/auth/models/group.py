from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy_utils import UUIDType
from sqlalchemy.sql import func
from uuid import uuid4
from database.base_class import Base


class Group(Base):

    __tablename__ = "auth_group"

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

    name = Column(String(255))

    def __str__(self):
        return f"Group {self.name}"

    def __repr__(self):
        return f"Group {self.name}"

    __mapper_args__ = {
    }
