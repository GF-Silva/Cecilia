from fastapi import APIRouter
from pydantic import BaseModel
from cecilia.integrations.groq import LLM
from cecilia.core.settings import settings

class PromptRequest(BaseModel):
    prompt: str

router = APIRouter()
llm = LLM(settings.groq.system_prompt)

@router.post("/")
async def send_promt(request: PromptRequest):
    return await llm.send_prompt(request.prompt)

@router.get("/")
async def get_context():
    return llm.context