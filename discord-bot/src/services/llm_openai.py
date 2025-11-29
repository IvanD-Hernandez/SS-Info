from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from .llm_base import baseLLMService

class OpenAILLMService(baseLLMService):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> str:
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            **kwargs,
        )
        return resp.choices[0].message.content or ""
