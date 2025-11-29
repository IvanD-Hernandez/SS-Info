from typing import Literal
from .llm_base import baseLLMService
from .llm_openai import OpenAILLMService
from .llm_ollama import OllamaLLMService

backendType = Literal["openai", "ollama"]

class llmManager:
    def __init__(
            self,
            backend: backendType,
            _api_key: str | None = None,
            gpt_model: str = "gpt-4o-mini",
            ollama_model: str = "llama3",
            ollama_url: str = "http://ollama:11434"
            ):
        
        self._backends: dict[backendType,baseLLMService] = {}

        if _api_key:
            self._backends["openai"] = OpenAILLMService(_api_key, gpt_model)

        self._backends["ollama"] = OllamaLLMService(ollama_url,ollama_model)

        self.active: backendType = backend

    def set_active(self, backend: backendType):
        if backend not in self._backends:
            raise ValueError(f"Backend {backend} not supported")
        self.active = backend

    @property
    def service(self) -> baseLLMService:
        return self._backends[self.active]
