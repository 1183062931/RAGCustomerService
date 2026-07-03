from abc import ABC, abstractmethod
from typing import Iterator


LLMMessage = dict[str, str]


class BaseChatProvider(ABC):
    def __init__(self, model: str) -> None:
        self.model = model

    @abstractmethod
    def chat(self, messages: list[LLMMessage], temperature: float = 0.2) -> str:
        raise NotImplementedError

    @abstractmethod
    def stream_chat(
        self, messages: list[LLMMessage], temperature: float = 0.2
    ) -> Iterator[str]:
        raise NotImplementedError
