from contextlib import asynccontextmanager
from aiobotocore.session import get_session


class S3Client:
    def __init__(self, access_key, secret_key, endpoint_url, bucket_name, public_endpoint_url=None):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.public_endpoint_url = public_endpoint_url or endpoint_url
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self, public: bool = False):
        config = self.config.copy()
        if public:
            config["endpoint_url"] = self.public_endpoint_url
        async with self.session.create_client("s3", **config) as client:
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

    async def download_bytes(self, key: str) -> bytes:
        async with self.get_client() as client:
            obj = await client.get_object(Bucket=self.bucket_name, Key=key)
            return await obj["Body"].read()

    async def delete_object(self, key: str):
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=key)

    async def list_objects(self, prefix: str = "") -> list[dict]:
        result = []
        async with self.get_client() as client:
            paginator = client.get_paginator("list_objects_v2")
            async for page in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix):
                for obj in page.get("Contents", []):
                    result.append({
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "last_modified": obj["LastModified"].isoformat(),
                    })
        return result

    async def presigned_url(self, key: str, expires_in: int = 3600, method: str = "get_object") -> str:
        async with self.get_client(public=True) as client:
            return await client.generate_presigned_url(
                ClientMethod=method,
                Params={"Bucket": self.bucket_name, "Key": key},
                ExpiresIn=expires_in,
            )
