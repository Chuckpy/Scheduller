import enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Enum
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy.orm import relationship

from .base_mixins import BaseMixin


class CashFlowType(enum.Enum):
    entry = 1
    exit = 2


class CashFlow(BaseMixin):
    
    __tablename__ = "core_cash_flow"

    id = Column(
        Integer, 
        ForeignKey("core_base_mixin.id"), 
        primary_key=True, 
        index=True,
        )
    
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
        "polymorphic_identity": "core_cash_flow",
    }
