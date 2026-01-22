from fastapi import APIRouter

from app.models.chat import ChatRequest, ChatResponse
from app.core.llm_client import LLMClient

router = APIRouter()
llm = LLMClient()  # simple singleton for now

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    content = await llm.chat(request.messages)
    return ChatResponse(content=content, model=llm.model)
