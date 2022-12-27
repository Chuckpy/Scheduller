from fastapi import APIRouter, Depends
from .services.task_services import TaskController
from core.schemas.task_schema import TaskCreateSchema, TaskSchema


router = APIRouter(
    prefix="/tasks", 
    tags=["tasks"] ,
)


@router.get("/")
async def list_tasks(tc: TaskController = Depends()):
    tasks =  tc.list_tasks()
    return tasks


# @router.get("/{task_id}")
# async def detailed_task(tc: TaskController = Depends()):
#     tasks =  tc.list_tasks()
#     return tasks


@router.post("/")
async def create_task(task_form: TaskCreateSchema, tc: TaskController = Depends()):
    task = tc.create_task(task_form)
    return task # TODO schema to display
    
