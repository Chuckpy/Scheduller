from core.models.tasks import Task
from core.apps.auth.services.user_services import UserController
from core.utils.paginator import Paginator
from fastapi import HTTPException, status, Request, Depends, Header
from database.db import get_session
from sqlalchemy.orm import Session



class TaskController(UserController):

    model = Task

    def __init__(
        self,
        request: Request,
        authorization: str | None = Header(),
        session: Session = Depends(get_session),
        limit: int = 10,
        per_page: int = 100,
        page: int = 1,
    ):

        self.request = request
        self.authorization = authorization.split(" ")[1]
        self.session = session
        self.limit = limit
        self.per_page = per_page
        self.page = page
        self._paginator = Paginator

    def list_tasks(self):
        user_id = self._get_user(self.authorization).id        
        tasks = (
            self.session.query(self.model)
            .filter(self.model.user_id == user_id)
            .limit(self.limit)
            .all()
        )
        paged_data = self._paginator(tasks, self.per_page, self.request).page(self.page)
        
        return paged_data

    def create_task(self, task_form):
        user_id = self._get_user(self.authorization).id
        task_form_dict = task_form.dict()
        task_form_dict["user_id"] = user_id
        db_task = self.model(**(task_form_dict))

        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)

        return db_task
