from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, status
from botocore.exceptions import ClientError

from ..schemas.file import FileSchemaAdd
from ..services.S3Client import S3Client
from app.config import settings


router = APIRouter(prefix="/file", tags=["File"])


def _make_client() -> S3Client:
    return S3Client(
        access_key=settings.ACCESS_KEY,
        secret_key=settings.SECRET_KEY_S3,
        endpoint_url=settings.ENDPOINT_URL,
        public_endpoint_url=settings.PUBLIC_ENDPOINT_URL,
        bucket_name=settings.BUCKET_NAME,
    )


def _http_error(e: ClientError) -> HTTPException:
    code = e.response.get("Error", {}).get("Code", "Unknown")
    if code in ("NoSuchKey", "404"):
        return HTTPException(status_code=404, detail="File not found")
    if code == "NoSuchBucket":
        return HTTPException(status_code=500, detail="S3 bucket does not exist")
    return HTTPException(status_code=502, detail=f"S3 error: {code}")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_file(payload: Annotated[FileSchemaAdd, Form()]):
    s3 = _make_client()
    data = await payload.file_upload.read()
    key = payload.file_upload.filename or payload.file_name
    try:
        await s3.upload_bytes(data=data, key=key, content_type=payload.file_upload.content_type)
    except ClientError as e:
        raise _http_error(e)
    return {"key": key}


@router.get("/")
async def list_files(prefix: str = ""):
    s3 = _make_client()
    try:
        return await s3.list_objects(prefix=prefix)
    except ClientError as e:
        raise _http_error(e)


@router.get("/url")
async def get_download_url(key: str, expires_in: int = 3600):
    s3 = _make_client()
    try:
        url = await s3.presigned_url(key=key, expires_in=expires_in)
    except ClientError as e:
        raise _http_error(e)
    return {"url": url, "expires_in": expires_in}


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(key: str):
    s3 = _make_client()
    try:
        await s3.delete_object(key=key)
    except ClientError as e:
        raise _http_error(e)
