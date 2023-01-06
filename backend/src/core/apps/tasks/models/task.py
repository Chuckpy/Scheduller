from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from database.base_model import BaseModel


class Task(BaseModel):

    __tablename__ = "task"

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
