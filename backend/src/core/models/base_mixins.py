from sqlalchemy import Boolean, Column, Integer, DateTime, String
from sqlalchemy.sql import func

from database import Base


class BaseMixin(Base):

    __tablename__ = "core_base_mixin"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
        )

    typing = Column(
        String(50)
        )

    created = Column(
        DateTime(timezone=True),
        server_default=func.now()
        )

    updated = Column(
        DateTime(timezone=True), 
        onupdate=func.now()
        )

    is_active = Column(Boolean, default=True)

    __mapper_args__ = {
        "polymorphic_identity": "core_base_mixin",
        "polymorphic_on": typing,
    }


# class ContentType(Base):

#     __tablename__ = "core_content_type"

#     id = Column(Integer, primary_key=True, index=True)
#     app_label = Column(String(255))
#     model = Column(String(255))
#     name = Column(String(255))

#     def __str__(self):
#         return f"Content Type {self.app_label}-{self.model}"

#     def __repr__(self):
#         return f"Content Type {self.app_label}-{self.model}"
