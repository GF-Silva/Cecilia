from cecilia.policies import AttachmentsAccessPolicy, MessageAccessPolicy, ChatAccessPolicy
from cecilia.services import AttachmentService, ChatService, MessageService
import uuid

class AttachmentCreateFacade:
    def __init__(
        self,
        attachment_access_policy: AttachmentsAccessPolicy,
        message_access_policy: MessageAccessPolicy,
        chat_access_policy: ChatAccessPolicy,
        attachment_service: AttachmentService,
        chat_service: ChatService,
        message_service: MessageService
    ):
        self.chat_access_policy = chat_access_policy
        self.message_access_policy = message_access_policy
        self.attachment_access_policy = attachment_access_policy
        self.chat_service = chat_service
        self.message_service = message_service

    def __call__(
        self,
        user_id: int,
        chat_id: uuid.UUID,
        message_id: int
    ):
        # This is just a placeholder class, so the tests works while it is not finished
        return
