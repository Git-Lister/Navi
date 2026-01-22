from typing import List
import ollama

from app.models.chat import Message  # absolute import

class LLMClient:
    def __init__(self, model: str = "deepseek-r1:32b"):
        self.model = model

    async def chat(self, messages: List[Message]) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[m.model_dump() for m in messages],
        )
        return response["message"]["content"]
