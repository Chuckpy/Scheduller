from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from database.base_model import BaseModel


class ListTextLine(BaseModel):

    __tablename__ = "list_text_line"

    content = Column(String(500))

    status = Column(Boolean, default=False, nullable=True)

    list_id = Column(
        ForeignKey("list.id"),
        nullable=False,
    )

    list = relationship("List", backref="list_text_lines", foreign_keys=[list_id])

    def __str__(self):
        return f"List Text Line #{self.id}"

    def __repr__(self):
        return f"List Text Line #{self.id}"

    __mapper_args__ = {}
