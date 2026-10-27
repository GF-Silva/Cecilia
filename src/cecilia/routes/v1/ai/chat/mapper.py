from .schemas import AudioPayload, ContentsPayload
from cecilia.integrations.open_router.types import Contents as OpenRouterContents, ContentsAudio
from pydantic import TypeAdapter

def to_openrouter_audio(audio: AudioPayload) -> ContentsAudio:
    return ContentsAudio(
        data = audio.data,
        format = audio.format
    )

def to_multi_openrouter_audio(audios: list[AudioPayload] | None) -> list[ContentsAudio]:
    adapter = TypeAdapter(list[ContentsAudio])
    return adapter.validate_python(audios)

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