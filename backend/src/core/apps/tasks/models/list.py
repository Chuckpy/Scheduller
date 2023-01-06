from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from database.base_model import BaseModel


class List(BaseModel):

    __tablename__ = "list"

    task_id = Column(
        ForeignKey("task.id"),
        nullable=False,
    )
    task = relationship("Task", backref="lists", foreign_keys=[task_id])

    def __str__(self):
        return f"List #{self.id}"

    def __repr__(self):
        return f"List #{self.id}"

    __mapper_args__ = {}
