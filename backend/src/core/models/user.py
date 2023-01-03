from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .tasks import Task

from .base_mixins import BaseMixin


class Group(BaseMixin):

    __tablename__ = "group"

    id = Column(Integer, ForeignKey("core_base_mixin.id"), primary_key=True, index=True)
    name = Column(String(255))

    def __str__(self):
        return f"Group {self.name}"

    def __repr__(self):
        return f"Group {self.name}"

    __mapper_args__ = {
        "polymorphic_identity": "group",
    }


class User(BaseMixin):

    __tablename__ = "users"

    id = Column(Integer, ForeignKey("core_base_mixin.id"), primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    full_name = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255))
    group_id = Column(Integer, ForeignKey("group.id"))
    group = relationship("Group", backref="users", foreign_keys=[group_id])
    tasks = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete",
        foreign_keys=[Task.user_id],
    )

    def __str__(self):
        return f"User #{self.id} - {self.first_name}"

    def __repr__(self):
        return f"User #{self.id} - {self.first_name}"

    __mapper_args__ = {
        "polymorphic_identity": "users",
    }
