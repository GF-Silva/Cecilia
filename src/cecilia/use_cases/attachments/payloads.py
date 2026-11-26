from pydantic import BaseModel
import uuid

class AttachmentShowPayload(BaseModel):
    user_id: int
    chat_id: uuid.UUID
    message_id: int
    attachment_id: int
