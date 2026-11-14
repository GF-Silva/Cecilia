from .image_validator import ImageValidator
from .audio_validator import AudioValidator
from cecilia.adapters import FFProbeAdapterDep
from typing import Annotated
from fastapi import Depends

def get_image_validator():
    return ImageValidator()

def get_audio_validator(
    ffprobe_adapter: FFProbeAdapterDep
):
    return AudioValidator(ffprobe_adapter=ffprobe_adapter)

ImageValidatorDep = Annotated[
    ImageValidator,
    Depends(get_image_validator)
]

AudioValidatorDep = Annotated[AudioValidator, Depends(get_audio_validator)]