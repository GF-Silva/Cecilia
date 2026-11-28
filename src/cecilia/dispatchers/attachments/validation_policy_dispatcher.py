from .errors import UnsupportedFileFormatError
from cecilia.policies import AttachmentImageValidationPolicy, AttachmentAudioValidationPolicy
from io import BufferedIOBase

class AttachmentValidationPolicyDispatcher:
    def __init__(
        self,
        attachment_image_validation_policy: AttachmentImageValidationPolicy,
        attachment_audio_validation_policy: AttachmentAudioValidationPolicy
    ):
        self.attachment_image_validation_policy=attachment_image_validation_policy
        self.attachment_audio_validation_policy=attachment_audio_validation_policy

    def __call__(self, mime_type: str, file: BufferedIOBase, size: int):
        if mime_type.startswith('audio/'):
            return self.attachment_audio_validation_policy(file=file, size=size)

        elif mime_type.startswith('image/'):
            return self.attachment_image_validation_policy(file=file, size=size)

        raise UnsupportedFileFormatError(format=mime_type)