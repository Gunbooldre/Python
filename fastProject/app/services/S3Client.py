from contextlib import asynccontextmanager
from aiobotocore.session import get_session


class S3Client:
    def __init__(self, access_key, secret_key, endpoint_url, bucket_name):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file_path, file_name):
        file_name = file_name.replace("\\", "/")
        async with self.get_client() as client:
            with open(file_path, "rb") as file:
                await client.put_object(Bucket=self.bucket_name, Key=file_name, Body=file)

    async def upload_bytes(self, data: bytes, key: str, content_type: str | None = None):
        key = key.replace("\\", "/")
        kwargs = {"Bucket": self.bucket_name, "Key": key, "Body": data}
        if content_type:
            kwargs["ContentType"] = content_type
        async with self.get_client() as client:
            await client.put_object(**kwargs)
