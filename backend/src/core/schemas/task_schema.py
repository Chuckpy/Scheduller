from datetime import datetime, date
from pydantic import BaseModel
from uuid import UUID


class TaskSchema(BaseModel):
    id: UUID = None
    description: str


class ListTextLineSchema(BaseModel):
    list_id: UUID | None
    content: str
    status: bool = False

    class Config:
        orm_mode = True


class ListSchema(BaseModel):
    task_id: UUID | None
    list_text_lines: list[ListTextLineSchema] = None

    class Config:
        orm_mode = True


class TextLineSchema(BaseModel):
    task_id: UUID | None
    content: str

    class Config:
        orm_mode = True


class TaskBaseSchema(BaseModel):
    description: str = ""
    deadline: datetime = None


class TaskDisplaySchema(TaskSchema):
    created: datetime
    deadline: datetime | date = None
    lists: list[ListSchema] = None
    text_lines: list[TextLineSchema] = None


class TaskCreateSchema(TaskSchema):
    deadline: datetime = None
    lists: list[ListSchema] | None = None
    text_lines: list[TextLineSchema] | None = None

    class Config:
        orm_mode = True
