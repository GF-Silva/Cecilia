from typing import BinaryIO
from cecilia.validators import ImageValidator
from cecilia.policies.validators.errors import FileTooBigError

class AttachmentImageValidationPolicy:
    _MAX_SIZE = 20_000_000
    
    def __init__(self, image_validator: ImageValidator):
        self.image_validator = image_validator
        
    def __call__(self, file: BinaryIO, size: int): 
        if size > self._MAX_SIZE:
            raise FileTooBigError(size=size, max_size=self._MAX_SIZE, resource='attachments')

        self.image_validator(stream=file)