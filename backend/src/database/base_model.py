from .base_class import Base
from sqlalchemy import Boolean, Column, DateTime 
from sqlalchemy_utils import UUIDType
from sqlalchemy.sql import func
from uuid import uuid4



class BaseModel(Base):

    __abstract__ = True

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