from types_aiobotocore_s3 import S3Client
from aiobotocore.session import get_session
from contextlib import AsyncExitStack

class R2Manager:
    def __init__(self):
        self.client = None
        self.exit_stack = AsyncExitStack()

    async def startup(
        self,
        account_id: str,
        access_key: str,
        secret_key: str,
        region_name: str
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

    async def list_files(self, bucket: str):
        files = await self.client.list_objects_v2(Bucket=bucket)

        if not files:
            raise ValueError("sla")

        return files

    async def create_file(
        self, 
        data: bytes,
        path: str,
        bucket: str
    ):
        try:
            await self.client.put_object(
                Bucket=bucket,
                Key=path,
                Body=data
            )
        
        except Exception as err:
            print("Erro: ", type(err))