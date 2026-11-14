from . import AttachmentService
from fastapi import Depends
from typing import Annotated
from cecilia.repositories.dependencies import AttachmentRepositoryDep

def get_attachment_service(
    attachment_repo: AttachmentRepositoryDep
):
    return AttachmentService(attachment_repo)

AttachmentServiceDep = Annotated[AttachmentService, Depends(get_attachment_service)]