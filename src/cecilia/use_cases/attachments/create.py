from cecilia.facades import AttachmentCreateFacade
from cecilia.extractors import FileMetadataExtractor
from cecilia.dispatchers import AttachmentValidationPolicyDispatcher
from cecilia.services import AttachmentService
from cecilia.models import AttachmentCreate, AttachmentPublic
from cecilia.integrations import R2
from .payloads import AttachmentCreatePayload

class AttachmentCreateUseCase:
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

        file_metadata = self.file_metada_extractor(file=payload.file)
        
        self.validation_policy_dispatcher(
            file=payload.file,
            mime_type=file_metadata.mime_type,
            size=file_metadata.size
        )

        attachment_create = AttachmentCreate(
            mime_type=file_metadata.mime_type, 
            size=file_metadata.size, 
            message_id=payload.message_id, 
            public_filename=payload.filename, 
            is_valid=True
        )
        
        db_attachment = self.service.create(
            message_id=payload.message_id,
            attachment=attachment_create
        )

        await self.r2_integration.create_file(
            data = payload.file.read(),
            path = attachment_create.path
        )

        return AttachmentPublic.model_validate(db_attachment.model_dump())