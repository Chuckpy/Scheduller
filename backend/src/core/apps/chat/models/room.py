from database.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from core.apps.chat.models import Message


class Room(BaseModel):

    __tablename__ = "chat_room"

    name = Column(String(255))

    description = Column(String(255))

    messages = relationship(
        "Message",
        back_populates="room",
        foreign_keys=[Message.room_id],
    )

    user_id = Column(
        ForeignKey("users.id"),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="rooms",
        foreign_keys=[user_id],
    )
