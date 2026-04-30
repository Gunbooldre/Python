from typing import Annotated
from fastapi import Form, UploadFile
from pydantic import BaseModel, ConfigDict


class FileSchemaAdd(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    file_name: str
    file_upload: UploadFile
