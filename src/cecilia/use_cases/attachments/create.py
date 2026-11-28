from cecilia.facades import AttachmentCreateFacade
from cecilia.extractors import FileMetadataExtractor
from cecilia.dispatchers import AttachmentValidationPolicyDispatcher
from cecilia.services import AttachmentService
from cecilia.models import AttachmentCreate, AttachmentPublic
from cecilia.integrations import R2
from .payloads import AttachmentCreatePayload, File
from pydantic import TypeAdapter

class AttachmentCreateUseCase:
    _ADAPTER = TypeAdapter(list[AttachmentPublic])

    def __init__(
        self,
        create_facade: AttachmentCreateFacade,
        file_metada_extractor: FileMetadataExtractor,
        validation_policy_dispatcher: AttachmentValidationPolicyDispatcher,
        service: AttachmentService,
        r2_integration: R2
    ):
        self.create_facade=create_facade
        self.file_metada_extractor=file_metada_extractor
        self.validation_policy_dispatcher=validation_policy_dispatcher
        self.service=service
        self.r2_integration=r2_integration
    
    async def __call__(self, payload: AttachmentCreatePayload):
        self.create_facade(
            user_id=payload.user_id,
            chat_id=payload.chat_id,
            message_id=payload.message_id
        )

        attachments_create: list[AttachmentCreate] = []
        for file in payload.files:
            attachments_create.append(await self._handle_file(file=file, message_id=payload.message_id))

        db_attachments = self.service.create_list(
            message_id=payload.message_id,
            attachments=attachments_create
        )

        return self._ADAPTER.validate_python(db_attachments)

    async def _handle_file(self, file: File, message_id: int):
        file_metadata = self.file_metada_extractor(file=file.stream)
                    
        self.validation_policy_dispatcher(
            file=file.stream,
            mime_type=file_metadata.mime_type,
            size=file_metadata.size
        )

        attachment_create = AttachmentCreate(
            mime_type=file_metadata.mime_type, 
            size=file_metadata.size, 
            message_id=message_id, 
            public_filename=file.filename, 
            is_valid=True
        )
        
        await self.r2_integration.create_file(
            data = file.stream.read(),
            path = attachment_create.path
        )

        return attachment_create
