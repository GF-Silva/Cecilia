from pydantic import BaseModel, ConfigDict
import uuid
from io import BufferedIOBase

class AttachmentShowPayload(BaseModel):
    user_id: int
    chat_id: uuid.UUID
    message_id: int
    attachment_id: int

class AttachmentCreatePayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    user_id: int
    chat_id: uuid.UUID
    message_id: int
    file: BufferedIOBase
    filename: str | None = None
