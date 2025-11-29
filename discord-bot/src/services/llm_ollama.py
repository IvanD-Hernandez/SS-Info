from typing import List, Dict, Any, Optional
import aiohttp
from .llm_base import baseLLMService

class OllamaLLMService(baseLLMService):
    def __init__(self, base_url: str = "http://127.0.0.1:11434", model: str = "llama3"):
        self.base_url = base_url
        self.model = model

    async def generate(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> str:

        prompt_parts = []
        for m in messages:
            role = m["role"]
            content = m["content"]
            prompt_parts.append(f"{role.upper()}: {content}")
        prompt_parts.append("ASSISTANT:")
        prompt = "\n".join(prompt_parts)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if max_tokens is not None:
            payload["num_predict"] = max_tokens

        async with aiohttp.ClientSession() as s:
            async with s.post(f"{self.base_url}/api/generate", json=payload) as r:
                data = await r.json()
                return data.get("response", "")
