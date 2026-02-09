from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from ..dependencies.dependencies import tasks_services
from ..schemas.task import TaskSchemaAdd
from ..services.task import TaskService


router = APIRouter(prefix="/task", tags=["Task"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
        task: TaskSchemaAdd,
        task_service: Annotated[TaskService, Depends(tasks_services)],
):
    task_id = await task_service.add_task(task)
    return {"task_id": task_id}
