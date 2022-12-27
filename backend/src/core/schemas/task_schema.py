from datetime import datetime
from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int = None
    description: str


class ListTextLineSchema(BaseModel):
    list_id: int | None
    content: str
    status: bool = False


class ListSchema(BaseModel):
    task_id: int | None
    list_text_lines: list[ListTextLineSchema] = None


class TextLineSchema(BaseModel):
    task_id: int | None
    content: str


class TaskCreateSchema(BaseModel):
    description: str = ""
    deadline: datetime = None


class TaskDisplaySchema(TaskSchema):
    created: datetime
    deadline: datetime = None
    lists: list[ListSchema] = None
    text_lines: list[TextLineSchema] = None


class TaskCreateSchema(TaskSchema):
    deadline: datetime = None
    lists: list[ListSchema] = None
    text_lines: list[TextLineSchema] = None
