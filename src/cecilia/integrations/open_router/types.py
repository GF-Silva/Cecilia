from dataclasses import dataclass

@dataclass
class ContentsAudios:
    format: str
    data: str

@dataclass
class Contents:
    prompt: str | None = None
    audios: list[ContentsAudios] | None = None
    images: list[ContentsAudios] | None = None