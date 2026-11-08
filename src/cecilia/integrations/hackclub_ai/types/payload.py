from enum import StrEnum
from typing import Literal, Annotated
from pydantic import BaseModel, Field

class CompletionTokensDetails(BaseModel):
    reasoning_tokens: int
    image_tokens: int
    audio_tokens: int

class CostDetails(BaseModel):
    upstream_inference_cost: float
    upstream_inference_prompt_cost: float
    upstream_inference_completions_cost: float

class PromptTokensDetails(BaseModel):
    cached_tokens: int
    cache_write_tokens: int
    audio_tokens: int
    video_tokens: int

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float
    is_byok: bool
    prompt_tokens_details: PromptTokensDetails
    cost_details: CostDetails
    completion_tokens_details: CompletionTokensDetails

class BaseReasoningDetails(BaseModel):
    id: str | None = None
    index: int | None = None
    format: str

class SummaryReasoning(BaseReasoningDetails):
    type: Literal['reasoning.summary'] = 'reasoning.summary'
    summary: str

class EncryptedReasoning(BaseReasoningDetails):
    type: Literal["reasoning.encrypted"] = "reasoning.encrypted"
    data: str

class TextReasoning(BaseReasoningDetails):
    type: Literal['reasoning.text'] = 'reasoning.text'
    text: str | None = None
    signature: str | None = None

ReasoningDetails = Annotated[
    TextReasoning | EncryptedReasoning | SummaryReasoning,
    Field(discriminator='type')
]

class Delta(BaseModel):
    content: str
    role: str
    reasoning: str | None = None
    reasoning_details: list[ReasoningDetails] | None = None

class FinishReason(StrEnum):
    TOOL_CALLS = "tool_calls"
    STOP = "stop"
    LENGTH = "length"
    CONTENT_FILTER = "content_filter"
    ERROR = "error"

class Choice(BaseModel):
    index: int
    delta: Delta
    finish_reason: FinishReason | None = None
    native_finish_reason: str | None = None

class CompletionEvent(BaseModel):
    id: str
    object: str
    created: int
    model: str
    provider: str
    choices: list[Choice]
    service_tier: str | None = None
    usage: Usage | None = None