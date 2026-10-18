from sqlmodel import Field, SQLModel

class AttachmentBase(SQLModel):
    type: str
    data: str
    size: str | None = Field(default=None)
    message_id: int

class Attachment(AttachmentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: str | None = Field(default="2020-01-20")

class AttachmentPublic(AttachmentBase):
    id: int
    created_at: str | None

class AttachmentCreate(AttachmentBase):
    pass