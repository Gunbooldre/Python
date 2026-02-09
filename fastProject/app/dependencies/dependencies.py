from app.repositories.task import TaskRepository
from app.services.task import TaskService


def tasks_services():
    return TaskService(TaskRepository)
