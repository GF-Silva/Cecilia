from .image_validator import ImageValidator
from cecilia.services.dependencies import AttachmentServiceDep
from typing import Annotated
from fastapi import Depends

def get_image_validator(
    attachment_service: AttachmentServiceDep
):
    return ImageValidator(attachment_service)

ImageValidatorDep = Annotated[
    ImageValidator,
    Depends(get_image_validator)
]