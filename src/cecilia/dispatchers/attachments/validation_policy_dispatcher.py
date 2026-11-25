from .errors import UnsupportedFileFormatError
from cecilia.policies.validators import AttachmentImageValidationPolicy, AttachmentAudioValidationPolicy
from typing import BinaryIO

class AttachmentValidationPolicyDispatcher:
    def __init__(
        self,
        attachment_image_validation_policy: AttachmentImageValidationPolicy,
        attachment_audio_validation_policy: AttachmentAudioValidationPolicy
    ):
        self.attachment_image_validation_policy=attachment_image_validation_policy
        self.attachment_audio_validation_policy=attachment_audio_validation_policy

    def __call__(self, mime_type: str, file: BinaryIO):
        if mime_type.startswith('audio/'):
            self.attachment_audio_validation_policy(file=file)

        elif mime_type.startswith('image/'):
            self.attachment_image_validation_policy(file=file)
