from sqlalchemy import Column, String
from database.base_model import BaseModel


class Group(BaseModel):

    __tablename__ = "auth_group"

    name = Column(String(255))

    def __str__(self):
        return f"Group {self.name}"

    def __repr__(self):
        return f"Group {self.name}"

    __mapper_args__ = {}
