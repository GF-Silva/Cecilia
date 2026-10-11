from fastapi import APIRouter
from pydantic import BaseModel
from src.cecilia.integrations.groq import LLM

class PromptRequest(BaseModel):
    prompt: str

router = APIRouter()
llm = LLM()

@router.post("/")
async def send_promt(request: PromptRequest):
    return await llm.send_prompt(request.prompt)

@router.get("/")
async def get_context():
    return llm.context