from pydantic import BaseModel


class PageSchema(BaseModel):

    page_number: int = 1
    next_page_url: str | None = None
    previous_page_url: str | None = None
    per_page: int = 0
    from_num: int = 0
    to_num: int = 0
    count: int
    data: list = []
