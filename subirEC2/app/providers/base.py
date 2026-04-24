from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, context: str, question: str) -> str:
        raise NotImplementedError
