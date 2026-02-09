from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int
    resposible_id: int

    class Config:
        from_attributes = True


class TaskSchemaAdd(TaskSchema):
    title: str
    description: str
    completed: bool

