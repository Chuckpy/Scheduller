from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from database.base_model import BaseModel


class TextLine(BaseModel):

    __tablename__ = "text_line"

    content = Column(String(500))

    task_id = Column(ForeignKey("task.id"))

    task = relationship("Task", backref="text_lines", foreign_keys=[task_id])

    def __str__(self):
        return f"Text Line #{self.id}"

    def __repr__(self):
        return f"Text Line #{self.id}"

    __mapper_args__ = {}
