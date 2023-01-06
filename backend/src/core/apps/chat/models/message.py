from database.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class Message(BaseModel):

    __tablename__ = "chat_message"

    room_id = Column(
        ForeignKey("chat_room.id"),
        nullable=False,
    )

    room = relationship(
        "Room",
        back_populates="messages",
        foreign_keys=[room_id],
    )

    content = Column(String(255))

    user_id = Column(
        ForeignKey("users.id"),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="messages",
        foreign_keys=[user_id],
    )
