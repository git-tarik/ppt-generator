from abc import ABC, abstractmethod

class LLMClient(ABC):
    @abstractmethod
    async def generate(self, prompt: str, api_key: str) -> str:
        """
        Generates a response from the LLM provider.
        Must handle its own HTTP calls and error mapping.
        """
        pass
