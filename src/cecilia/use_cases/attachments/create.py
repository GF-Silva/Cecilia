from cecilia.services import AttachmentService
from cecilia.core.settings import settings
from cecilia.models.attachment_model import AttachmentCreate
from cecilia.models.tables import Message
from cecilia.integrations.cloudflare.r2 import R2
from cecilia.validators import FileValidator
from cecilia.integrations.hackclub_ai.rules import ACCEPTED_MIME_TYPES

from dataclasses import dataclass
from fastapi import UploadFile

@dataclass
class FileData:
    file: UploadFile
    mime_type: str
    size: int
    filename: str | None = None

class CreateAttachmentsUseCase:
    def __init__(
        self,
        attachment_service: AttachmentService,
        r2_integration: R2,
        file_validator: FileValidator
    ):
        self.attachment_service = attachment_service
        self.r2_integration = r2_integration
        self.file_validator = file_validator

    async def __call__(
        self,
        message_id: int,
        message: Message,
        files: list[UploadFile],
    ):
        self.attachment_service.validate_message_role(message)
        files_data = await self._validate_files(files)
    
        attachments_create: list = []
        for file in files_data:
            await file.file.seek(0)
            attachment = AttachmentCreate(
                mime_type = file.mime_type,
                public_filename = file.filename,
                size = file.size,
                message_id = message_id
            )

            await self.r2_integration.create_file(
                data=await file.file.read(),
                path=attachment.path,
                bucket=settings.r2.bucket
            )
    
            attachments_create.append(attachment)
    
        db_attachments = self.attachment_service.create_list(
            attachments=attachments_create,
            message=message
        )
    
        return db_attachments

    async def _validate_files(self, files: list[UploadFile]) -> list[FileData]:
        files_data: list[FileData] = []

        for file in files:
            validated_file = await self.file_validator(
                stream=file.file, 
                filename=file.filename, 
                max_size=self.r2_integration.MAX_FILE_SIZE,
                allowed_types=ACCEPTED_MIME_TYPES
            )
            assert validated_file.mime_type
            assert validated_file.size
            
            files_data.append(FileData(
                file=file,
                mime_type=validated_file.mime_type,
                size=validated_file.size,
                filename=file.filename
            ))

        return files_data

    