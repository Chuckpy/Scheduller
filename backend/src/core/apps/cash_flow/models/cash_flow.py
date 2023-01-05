from database.base_class import Base
from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime, Float, Enum
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
import enum


class CashFlowType(enum.Enum):
    entry = 1
    exit = 2


class CashFlow(Base):
    
    __tablename__ = "core_cash_flow"

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
    
    deadline = Column(
        DateTime(timezone=True),
        nullable = True,
    )

    description = Column(
        String(2000)
    )

    value = Column(
        Float(precision = 2),
        nullable=False,
    )

    type = Column(
        Enum(CashFlowType),
        nullable=False,
    )
    
    payment_date = Column(
        DateTime(timezone=True),
        nullable = True,
        default=None,
    )

    is_recurring = Column(
        Boolean(),
        default = False,
        nullable = False,
    )

    user_id = Column(
        ForeignKey("users.id"),
        nullable = False,
    )

    user = relationship(
        "User",
        back_populates = "cash_flows",
        foreign_keys = [user_id],
    )

    def __str__(self):
        return f"Cash Flow #{self.id}"

    def __repr__(self):
        return f"Cash Flow #{self.id}"

    __mapper_args__ = {
    }
