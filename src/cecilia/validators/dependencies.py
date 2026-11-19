from .image_validator import ImageValidator
from .audio_validator import AudioValidator
from .file import FileValidator
from cecilia.adapters import FFProbeAdapterDep
from typing import Annotated
from fastapi import Depends

def get_image_validator():
    return ImageValidator()

def get_audio_validator(
    ffprobe_adapter: FFProbeAdapterDep
):
    return AudioValidator(ffprobe_adapter=ffprobe_adapter)

def get_file_validator(
    audio_validator: AudioValidatorDep,
    image_validator: ImageValidatorDep
):
    return FileValidator(audio_validator=audio_validator, image_validator=image_validator)

ImageValidatorDep = Annotated[ImageValidator, Depends(get_image_validator)]
AudioValidatorDep = Annotated[AudioValidator, Depends(get_audio_validator)]
FileValidatorDep = Annotated[FileValidator, Depends(get_file_validator)]