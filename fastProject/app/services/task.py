from app.schemas.task import TaskSchemaAdd
from app.utils.repository import AbstractRepository


class TaskService:
    def __init__(self, task_repo: AbstractRepository):
        self.task_repo: AbstractRepository = task_repo()

    async def add_task(self, task: TaskSchemaAdd):
        task_dict = task.model_dump()
        task_id = await self.task_repo.add_one(task_dict)
        return task_id
