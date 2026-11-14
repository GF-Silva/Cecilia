from cecilia.services import AttachmentService
from cecilia.core.settings import settings
from cecilia.adapters.ffprobe.ffprobe_adapter import FFProbeAdapter
from cecilia.models.attachment_model import AttachmentCreate
from cecilia.models.tables import Message
from cecilia.integrations.cloudflare.r2 import R2
from cecilia.validators import ImageValidator, AudioValidator
from cecilia.core.exceptions import (
    UnsupportedFileFormatError, 
    FileTooBigError,
    InvalidFileError
)

from dataclasses import dataclass
from fastapi import UploadFile
import asyncio
import filetype

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
        ffprobe_adapter: FFProbeAdapter,
        image_validator: ImageValidator,
        audio_validator: AudioValidator
    ):
        self.attachment_service = attachment_service
        self.r2_integration = r2_integration
        self.ffprobe_adapter = ffprobe_adapter
        self.image_validator = image_validator
        self.audio_validator = audio_validator

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
            # Valida a extensao do arquivo
            self.attachment_service.validate_mime_type(file.headers['content-type'])
            file.size = file.size or 0

            # Valida o tamanho do arquivo
            if file.size > self.r2_integration.MAX_FILE_SIZE:
                raise FileTooBigError(
                    values = {
                        "size": file.size,
                        "filename": file.filename,
                        "max_file_size": self.r2_integration.MAX_FILE_SIZE
                    }
                )

            file_type = filetype.guess(await file.read(2048))

            if not file_type:
                raise InvalidFileError()
            
            files_data.append(FileData(
                file=file,
                mime_type=file_type.mime,
                size=file.size,
                filename=file.filename
            ))
            
            # TODO: Adicionar yield aq pra processar em paralelo
            if file_type.mime.startswith('audio/'):
                await asyncio.to_thread(self.audio_validator, file.file)

            elif file_type.mime.startswith('image/'):
                await asyncio.to_thread(self.image_validator, file.file)

            else:
                raise UnsupportedFileFormatError(
                    message="Unsuported file format",
                    values = {
                        "format": file_type,
                        "filename": file.filename
                    }
                )

        return files_data

    