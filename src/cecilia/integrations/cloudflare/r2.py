from types_aiobotocore_s3 import S3Client
from aiobotocore.session import get_session
from contextlib import AsyncExitStack
from cecilia.core.settings import settings
from cecilia.core.exceptions import FileNotFoundError, InternalError

class R2Manager:
    def __init__(self):
        self.client = None
        self.exit_stack = AsyncExitStack()

    async def startup(
        self,
        account_id: str = settings.r2.account_id,
        access_key: str = settings.r2.access_key,
        secret_key: str = settings.r2.secret_access_key,
        region_name: str = settings.r2.region
    ):
        session = get_session()
        endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"
    
        client_cm = session.create_client(
            's3',
            region_name=region_name,
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
    
        self.client = await self.exit_stack.enter_async_context(client_cm)

    async def shutdown(self):
        await self.exit_stack.aclose()

class R2:
    MAX_IMAGE_SIZE = 10 * 1024 * 1024 # 10 MB
    MAX_AUDIO_SIZE = 100 * 1024 * 1024 # 100 MB
    MAX_FILE_SIZE = 100 * 1024 * 1024 # 150 MB

    def __init__(self, client: S3Client):
        self.client = client

    async def list_files(self, bucket: str = settings.r2.bucket):
        files = await self.client.list_objects_v2(Bucket=bucket)

        return files

    async def get_file_data(self, path: str, bucket: str = settings.r2.bucket, max: int | None = None) -> bytes | None:
        try:
            file = await self.client.get_object(
                Bucket=bucket,
                Key=path
            )

            async with file['Body'] as stream:
                return await stream.read(max)

        except self.client.exceptions.NoSuchKey:
            raise FileNotFoundError(
                values={
                    "path": path
                }
            )

        except Exception as err:
            print("Erro: ", type(err))
            raise InternalError()

    async def create_file(
        self, 
        data: bytes,
        path: str,
        bucket: str = settings.r2.bucket
    ):
        try:
            await self.client.put_object(
                Bucket=bucket,
                Key=path,
                Body=data
            )
        
        except Exception as err:
            print("R2 Integration - error: ", type(err))
            raise InternalError()

    async def generate_presigned_get_url(
        self,
        path: str,
        bucket: str = settings.r2.bucket,
        expireTime: int = 3600
    ):
        try:
            return await self.client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": bucket,
                    "Key": path
                },
                ExpiresIn=expireTime
            )

        except self.client.exceptions.NoSuchKey:
            raise FileNotFoundError(
                values={
                    "path": path
                }
            )
        
        except Exception as err:
            print("Erro na r2: ", type(err))
            raise InternalError()