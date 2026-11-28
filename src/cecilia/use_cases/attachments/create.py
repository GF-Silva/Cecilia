from cecilia.facades import AttachmentCreateFacade
from cecilia.extractors import FileMetadataExtractor
from cecilia.dispatchers import AttachmentValidationPolicyDispatcher
from cecilia.services import AttachmentService
from cecilia.models import AttachmentCreate
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
    
    def __call__(self, payload: AttachmentCreatePayload):
        return True