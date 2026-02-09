from app.models.models import Task
from app.utils.repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = Task
    