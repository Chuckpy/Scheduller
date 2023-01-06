from fastapi import APIRouter, Path, Depends
from .services.task_services import TaskController
from core.schemas.task_schema import TaskCreateSchema, TaskBaseSchema


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/")
async def list_tasks(tc: TaskController = Depends()):
    tasks = tc.list_tasks()
    return tasks


@router.get("/{task_id}/")
async def detailed_task(
    task_id: int = Path(title="The ID of the Task"), tc: TaskController = Depends()
):
    task_detail = tc.get_retail_task(task_id)
    return task_detail


@router.put("/{task_id}/")
async def update_task(
    task_form: TaskBaseSchema,
    task_id: int = Path(title="The ID of the Task"),
    tc: TaskController = Depends(),
):

    tc.update_task(task_id, task_form)
    task_updated = tc.get_retail_task(task_id)

    return task_updated


@router.post("/")
async def create_task(task_form: TaskCreateSchema, tc: TaskController = Depends()):
    task = tc.create_task(task_form)
    return task
