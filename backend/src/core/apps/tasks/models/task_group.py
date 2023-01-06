from sqlalchemy import Column, String
from database.base_model import BaseModel


class TaskGroup(BaseModel):

    __tablename__ = "task_group"

    title = Column(String(255))

    def __str__(self):
        return f"Task Group #{self.id}"

    def __repr__(self):
        return f"Task Group #{self.id}"

    __mapper_args__ = {}
