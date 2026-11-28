from io import BufferedIOBase
from cecilia.validators import AudioValidator
from cecilia.policies.validators.errors import FileTooBigError

class AttachmentAudioValidationPolicy:
    _MAX_SIZE = 100_000_000
    
    def __init__(self, audio_validator: AudioValidator):
        self.audio_validator = audio_validator
        
    async def __call__(self, file: BufferedIOBase, size: int): 
        if size > self._MAX_SIZE:
            raise FileTooBigError(size=size, max_size=self._MAX_SIZE, resource='audios')

        await self.audio_validator(stream=file)