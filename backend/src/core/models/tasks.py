from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .base_mixins import BaseMixin


class TaskGroup(BaseMixin):

    __tablename__ = "task_group"

    id = Column(Integer, ForeignKey("core_base_mixin.id"), primary_key=True, index=True)
    title = Column(String(255))

    def __str__(self):
        return f"Task Group #{self.id}"

    def __repr__(self):
        return f"Task Group #{self.id}"

    __mapper_args__ = {
        "polymorphic_identity": "task_group",
    }


class Task(BaseMixin):

    __tablename__ = "task"

    id = Column(Integer, ForeignKey("core_base_mixin.id"), primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    user = relationship("User", back_populates="tasks", foreign_keys=[user_id])

    deadline = Column(
        DateTime,
        nullable=True,
    )

    description = Column(
        String(255),
        nullable=False,
    )

    task_group_id = Column(Integer, ForeignKey("task_group.id"), nullable=True)

    task_group = relationship(
        "TaskGroup", backref="tasks", foreign_keys=[task_group_id]
    )

    def __str__(self):
        return f"Task #{self.id}"

    def __repr__(self):
        return f"Task #{self.id}"

    __mapper_args__ = {
        "polymorphic_identity": "task",
    }


class List(BaseMixin):

    __tablename__ = "list"

    id = Column(Integer, ForeignKey("core_base_mixin.id"), primary_key=True, index=True)
    task_id = Column(
        Integer,
        ForeignKey("task.id"),
        nullable=False,
    )
    task = relationship("Task", backref="lists", foreign_keys=[task_id])

    def __str__(self):
        return f"List #{self.id}"

    def __repr__(self):
        return f"List #{self.id}"

    __mapper_args__ = {
        "polymorphic_identity": "list",
    }


class ListTextLine(BaseMixin):

    __tablename__ = "list_text_line"

    id = Column(Integer, ForeignKey("core_base_mixin.id"), primary_key=True, index=True)
    content = Column(String(500))
    status = Column(Boolean, default=False, nullable=True)
    list_id = Column(
        Integer,
        ForeignKey("list.id"),
        nullable=False,
    )
    list = relationship("List", backref="list_text_lines", foreign_keys=[list_id])

    def __str__(self):
        return f"List Text Line #{self.id}"

    def __repr__(self):
        return f"List Text Line #{self.id}"

    __mapper_args__ = {
        "polymorphic_identity": "list_text_line",
    }


class TextLine(BaseMixin):

    __tablename__ = "text_line"

    id = Column(Integer, ForeignKey("core_base_mixin.id"), primary_key=True, index=True)
    content = Column(String(500))
    task_id = Column(Integer, ForeignKey("task.id"))
    task = relationship("Task", backref="text_lines", foreign_keys=[task_id])

    def __str__(self):
        return f"Text Line #{self.id}"

    def __repr__(self):
        return f"Text Line #{self.id}"

    __mapper_args__ = {
        "polymorphic_identity": "text_line",
    }
