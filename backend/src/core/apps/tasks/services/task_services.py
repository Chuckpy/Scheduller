from core.apps.tasks.models import Task, List, TextLine, ListTextLine
from core.apps.auth.services.user_services import UserController
from core.utils.paginator import Paginator
from core.schemas.page_schema import PageSchema
from core.schemas.task_schema import (
    TaskDisplaySchema,
    ListSchema,
    TextLineSchema,
    ListTextLineSchema,
    TaskCreateSchema,
    TaskBaseSchema,
)
from fastapi import Request, Depends, Header, HTTPException
from database.db import get_session
from sqlalchemy.orm import Session
from uuid import uuid4, UUID



class TaskPaged(PageSchema):
    data: list[TaskDisplaySchema]


class TaskController(UserController):

    model = Task

    def __init__(
        self,
        request: Request,
        authorization: str | None = Header(),
        session: Session = Depends(get_session),
        limit: int = 100,
        per_page: int = 10,
        page: int = 1,
    ):

        self.request = request
        self.authorization = authorization.split(" ")[1]
        self.session = session
        self.limit = limit
        self.per_page = per_page
        self.page = page
        self._paginator = Paginator

    def get_task_by_id(self, task_id: int = None):

        task = self.session.query(self.model).filter(self.model.id == task_id).first()

        if task:
            return task

        raise HTTPException(status_code=404, detail="Task not found")

    def get_retail_task(self, task: Task | UUID = False):

        if type(task) == UUID:
            task = self.get_task_by_id(task)

        task_detailed = TaskDisplaySchema.parse_obj(task.__dict__)
        task_detailed.lists = [
            ListSchema.parse_obj(list.__dict__) for list in task.lists
        ]

        list_text_lines = [list.list_text_lines for list in task.lists]

        for index, list_text_lines in enumerate(list_text_lines):
            task_detailed.lists[index] = [
                ListTextLineSchema.parse_obj(text_line.__dict__)
                for text_line in list_text_lines
            ]

        task_detailed.text_lines = [
            TextLineSchema.parse_obj(text_line.__dict__)
            for text_line in task.text_lines
        ]

        return task_detailed

    def list_tasks(self):
        user_id = self._get_user(self.authorization).id
        tasks = (
            self.session.query(self.model)
            .filter(self.model.user_id == user_id)
            .limit(self.limit)
            .all()
        )
        page = self._paginator(tasks, self.per_page, self.request).page(self.page)

        paged_data = TaskPaged(
            page_number=page.number,
            per_page=len(page.object_list),
            count=len(tasks),
            from_num=page.start_index(),
            to_num=page.end_index(),
            next_page_url=page.get_next_link(),
            previous_page_url=page.get_previous_link(),
            data=[self.get_retail_task(obj) for obj in page.object_list],
        ).dict()

        return paged_data

    def create_lists_text_lines(self, list_text_line_form, list_id: int, user_id=None):
        if not user_id:
            user_id = self._get_user(self.authorization).id

        list_text_lines = []

        for list_text_line in list_text_line_form:
            list_text_line["list_id"] = list_id
            list_text_line["id"] = uuid4()
            db_list_text_line = ListTextLine(**list_text_line)
            self.session.add(db_list_text_line)
            self.session.commit()
            self.session.refresh(db_list_text_line)
            list_text_lines.append(db_list_text_line)

        return list_text_lines

    def create_lists(self, list_form, task_id: int, user_id=None):
        if not user_id:
            user_id = self._get_user(self.authorization).id

        lists = []

        for list in list_form:

            if "list_text_lines" in list:
                self.list_text_lines = list.pop("list_text_lines")

            list["task_id"] = task_id
            list["id"] = uuid4()
            db_list = List(**list)
            self.session.add(db_list)
            self.session.commit()
            self.session.refresh(db_list)
            lists.append(db_list)

        if self.list_text_lines:
            self.create_lists_text_lines(self.list_text_lines, db_list.id, user_id)

        return lists

    def create_text_lines(self, text_line_form, task_id: int, user_id=None):
        if not user_id:
            user_id = self._get_user(self.authorization).id

        text_lines = []
        for text_line in text_line_form:
            text_line["task_id"] = task_id
            text_line["id"] = uuid4()
            db_text_line = TextLine(**text_line)
            self.session.add(db_text_line)
            self.session.commit()
            self.session.refresh(db_text_line)
            text_lines.append(db_text_line)

        return text_lines

    def create_task(self, task_form: TaskCreateSchema):
        self.text_lines = []
        self.lists = []
        self.list_text_lines = []

        user_id = self._get_user(self.authorization).id

        task_form_dict = task_form.dict(exclude_none=True)
        to_return = task_form_dict.copy()
        task_form_dict["user_id"] = user_id
        task_form_dict["id"] = uuid4()

        if "text_lines" in task_form_dict.keys():
            self.text_lines = task_form_dict.pop("text_lines")

        if "lists" in task_form_dict.keys():
            self.lists = task_form_dict.pop("lists")

        db_task = self.model(**(task_form_dict))

        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)

        if self.text_lines:
            self.create_text_lines(self.text_lines, db_task.id, user_id)

        if self.lists:
            self.create_lists(self.lists, db_task.id, user_id)

        return self.get_retail_task(db_task.id)

    def update_task(self, task_id: int, task_form: TaskBaseSchema):

        task = self.get_task_by_id(task_id)

        task_form_dict = task_form.dict(exclude_none=True)

        task_query = self.session.query(task.__class__).filter(
            task.__class__.id == task_id
        )
        task_query.update(task_form_dict)
