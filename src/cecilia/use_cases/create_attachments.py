from cecilia.models.attachment_model import AttachmentCreate
from cecilia.integrations.cloudflare.r2 import R2
from cecilia.core.exceptions import (
    ValueError, 
    UnsupportedFileFormatError, 
    FileTooBigError,
    InvalidFileError,
    InternalError
)

from starlette.datastructures import Headers
from cecilia.services import AttachmentService
from cecilia.core.settings import settings
from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile
from uuid import uuid7
import asyncio
import magic

class CreateAttachmentsUseCase:
    def __init__(
        self,
        attachment_service: AttachmentService,
        r2_integration: R2,
    ):
        self.attachment_service = attachment_service
        self.r2_integration = r2_integration

    async def __call__(
        self,
        message_id: int,
        files: list[UploadFile],
    ):     
        attachments_create: list = []

        await self._validate_files(files)
    
        for file in files:
            mime_type = file.headers["content-type"]
            print(mime_type)

            await file.seek(0)  

            file_data = await file.read()
    
            internal_filename = uuid7()
            path = f"{mime_type}/{internal_filename}"
    
            await self.r2_integration.create_file(
                data=file_data,
                path=path,
                bucket=settings.r2.bucket
            )
    
            attachment = AttachmentCreate(
                mime_type = mime_type,
                public_filename = file.filename,
                size = file.size,
                message_id = message_id,
                filename=internal_filename,
                path=path
            )
    
            attachments_create.append(attachment)
    
        db_attachments = self.attachment_service.create_list(attachments_create)
    
        return db_attachments

    async def _validate_files(self, files: list[UploadFile]):
        mime = magic.Magic(mime=True)

        for file in files:
            # Valida a extensao do arquivo
            self.attachment_service.validate_mime_type(file.headers['content-type'])
            file.file.seek(0, 2)
            file_size = file.file.tell()

            # Valida o tamanho do arquivo
            if file_size > self.r2_integration.MAX_FILE_SIZE:
                raise FileTooBigError(
                    values = {
                        "size": file.size,
                        "filename": file.filename,
                        "max_file_file": self.r2_integration.MAX_FILE_SIZE
                    }
                )

            await file.seek(0)
            file_data = await file.read()

            # Valida se tem conteudo interno
            if not file_data:
                raise InvalidFileError(
                    message = "Empty file"
                )
        
            mime_type = mime.from_buffer(file_data)
            print(mime_type)

            self.attachment_service.validate_mime_type(mime_type)

            new_headers = dict(file.headers)
            new_headers["content-type"] = mime_type

            file.headers = Headers(new_headers)
