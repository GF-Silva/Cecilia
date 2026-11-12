from cecilia.services import AttachmentService
from cecilia.core.settings import settings
from cecilia.adapters.ffprobe.ffprobe_adapter import FFProbeAdapter
from cecilia.models.attachment_model import AttachmentCreate
from cecilia.models.tables import Message
from cecilia.integrations.cloudflare.r2 import R2
from cecilia.core.exceptions import (
    UnsupportedFileFormatError, 
    FileTooBigError,
    InvalidFileError,
    InternalError
)

from dataclasses import dataclass
from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile
import asyncio
import magic

@dataclass
class FileData:
    file: UploadFile
    mime_type: str
    size: int
    filename: str | None = None

class CreateAttachmentsUseCase:
    MIME_VALIDATOR = magic.Magic(mime=True)

    def __init__(
        self,
        attachment_service: AttachmentService,
        r2_integration: R2,
        ffprobe_adapter: FFProbeAdapter
    ):
        self.attachment_service = attachment_service
        self.r2_integration = r2_integration
        self.ffprobe_adapter = ffprobe_adapter

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

            await file.seek(0)
            file_data = await file.read()

            # Valida se tem conteudo interno
            if not file_data:
                raise InvalidFileError(
                    message = "Empty file"
                )

            mime_type = self.MIME_VALIDATOR.from_buffer(file_data)

            files_data.append(FileData(
                file=file,
                mime_type=mime_type,
                size=file.size,
                filename=file.filename
            ))
            
            # TODO: Adicionar yield aq pra processar em paralelo
            if mime_type.startswith('audio/'):
                await self._process_audio(file.size, file_data, file.filename)

            elif mime_type.startswith('image/'):
                await self._validate_image(file)

            else:
                raise UnsupportedFileFormatError(
                    message="Unsuported file format",
                    values = {
                        "format": mime_type,
                        "filename": file.filename
                    }
                )

        return files_data

    async def _process_audio(self, file_size: int, file_data: bytes, filename: str | None = None):
        if file_size > self.r2_integration.MAX_AUDIO_SIZE:
            raise FileTooBigError(
                values = {
                    "size": file_size,
                    "filename": filename,
                    "max_file_size": self.r2_integration.MAX_AUDIO_SIZE
                }
            )
        
        file_metadata = await self.ffprobe_adapter.validate_file_from_buffer(file_data)
        self.attachment_service.validate_file_type(file_metadata.format.format_name)
    
    async def _validate_image(self, file: UploadFile):
        if not file.size:
            raise InvalidFileError(
                message = "Empty file"
            )
        
        if file.size > self.r2_integration.MAX_IMAGE_SIZE:
            raise FileTooBigError(
                values = {
                    "size": file.size,
                    "filename": file.filename,
                    "max_file_size": self.r2_integration.MAX_FILE_SIZE
                }
            )
        
        try:
            with Image.open(file.file) as img:
                await asyncio.to_thread(img.verify)

        except UnidentifiedImageError:
            raise InvalidFileError()

        except Image.DecompressionBombError:
            raise FileTooBigError()

        except Exception as err:
            print("Attachments (CreateUseCase) - err: ", err)
            raise InternalError()