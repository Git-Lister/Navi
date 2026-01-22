from pydantic import BaseModel
from typing import List, Literal, Optional

Role = Literal["system", "user", "assistant"]

class Message(BaseModel):
    role: Role
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    content: str
    model: Optional[str] = None
