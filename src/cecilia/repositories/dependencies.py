from . import AttachmentRepository
from cecilia.core.database import SessionDep
from fastapi import Depends
from typing import Annotated

def get_attachment_repository(
    session: SessionDep
):
    return AttachmentRepository(session)

AttachmentRepositoryDep = Annotated[AttachmentRepository, Depends(get_attachment_repository)]