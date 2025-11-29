from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class baseLLMService(ABC):
    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> str:
        """
        messages: list of {"role": "user"/"system"/"assistant", "content": "..."}
        returns: assistant message content
        """
