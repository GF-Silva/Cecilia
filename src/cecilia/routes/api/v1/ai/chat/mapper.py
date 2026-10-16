from .schemas import AudioPayload, ContentsPayload
from cecilia.integrations.open_router.types import Contents as OpenRouterContents, ContentsAudios

def to_openrouter_audio(audio: AudioPayload) -> ContentsAudios:
    return ContentsAudios(
        data = audio.data,
        format = audio.format
    )

def to_openrouter_contents(contents: ContentsPayload) -> OpenRouterContents:
    openrouter_audios = (
        [to_openrouter_audio(audio) for audio in contents.audios]
        if contents.audios is not None
        else None
    )
    
    return OpenRouterContents(
        prompt = contents.prompt,
        audios = openrouter_audios,
        images = contents.images
    )