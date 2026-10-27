from dataclasses import dataclass
import json

@dataclass
class CompletionTokensDetails:
    reasoning_tokens: int
    image_tokens: int
    audio_tokens: int

@dataclass
class CostDetails:
    upstream_inference_cost: float
    upstream_inference_prompt_cost: float
    upstream_inference_completions_cost: float

@dataclass
class PromptTokensDetails:
    cached_tokens: int
    cache_write_tokens: int
    audio_tokens: int
    video_tokens: int

@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float
    is_byok: bool
    prompt_tokens_details: PromptTokensDetails
    cost_details: CostDetails
    completion_tokens_details: CompletionTokensDetails

@dataclass
class Delta:
    content: str
    role: str

    @classmethod
    def from_json(cls, json):
        return cls(
            content=json.get('content'),
            role=json.get('role')
        )

@dataclass
class Choice:
    index: int
    delta: Delta
    finish_reason: str | None = None
    native_finish_reason: str | None = None

    @classmethod
    def from_json(cls, json):
        return cls(
            index=json.get('index'),
            delta=Delta.from_json(json.get('delta')),
            finish_reason=json.get('finish_reason'),
            native_finish_reason=json.get('native_finish_reason')
        )

@dataclass
class SSEPayload:
    id: str
    object: str
    created: int
    model: str
    provider: str
    choices: list[Choice]
    service_tier: str | None = None
    usage: Usage | None = None

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)

        return cls(
            id=data.get("id"),
            object=data.get("object"),
            created=data.get("created"),
            model=data.get("model"),
            provider=data.get("provider"),
            choices=[
                Choice.from_json(choice)
                for choice in data.get("choices")
            ],
            service_tier=data.get("service_tier"),
            usage=data.get("usage")
        )