from cecilia.models.attachment_model import AttachmentCreate
from cecilia.integrations.cloudflare.r2 import R2
from cecilia.core.exceptions import ValueError
from cecilia.services import AttachmentService
from cecilia.core.settings import settings
from fastapi import UploadFile
from uuid import uuid7
import magic

class CreateAttachmentsUseCase:
    def __init__(
        self,
        attachment_service: AttachmentService,
        r2_integration: R2,
    ):
        self.attachment_service = attachment_service
        self.r2_integration = r2_integration

    async def execute(
        self,
        message_id: int,
        files: list[UploadFile],
    ):
        mime = magic.Magic(mime=True)
        
        attachments_create: list = []
    
        for file in files:
            await file.seek(0)
            file_data = await file.read()
            mime_type = mime.from_buffer(file_data)
            
            self.attachment_service.validate_mime_type(mime_type)
    
            if not file_data:
                raise ValueError(
                    message = "Invalid File Data",
                    error_code = "INVALID_FILE_DATA"
                )
    
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