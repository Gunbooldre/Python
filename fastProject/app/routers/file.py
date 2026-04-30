from typing import Annotated
from fastapi import APIRouter, Form, status

from ..schemas.file import FileSchemaAdd
from ..services.S3Client import S3Client
from app.config import settings


router = APIRouter(prefix="/file", tags=["File"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_file(payload: Annotated[FileSchemaAdd, Form()]):
    s3 = S3Client(
        access_key=settings.ACCESS_KEY,
        secret_key=settings.SECRET_KEY_S3,
        endpoint_url=settings.ENDPOINT_URL,
        bucket_name=settings.BUCKET_NAME,
    )
    data = await payload.file_upload.read()
    key = payload.file_upload.filename or payload.file_name
    await s3.upload_bytes(
        data=data,
        key=key,
        content_type=payload.file_upload.content_type,
    )
    return {"key": key}
