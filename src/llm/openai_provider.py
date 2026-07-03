from typing import Iterator

from openai import NotFoundError, OpenAI

from src.llm.base import BaseChatProvider, LLMMessage


class OpenAICompatibleChatProvider(BaseChatProvider):
    def __init__(self, model: str, api_key: str, base_url: str | None = None) -> None:
        super().__init__(model=model)
        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        self.client = OpenAI(**client_kwargs)

    def chat(self, messages: list[LLMMessage], temperature: float = 0.2) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
            )
            return response.choices[0].message.content or ""
        except NotFoundError:
            return self._chat_via_responses(messages)

    def stream_chat(
        self, messages: list[LLMMessage], temperature: float = 0.2
    ) -> Iterator[str]:
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                if token:
                    yield token
        except NotFoundError:
            yield from self._stream_via_responses(messages)

    def _chat_via_responses(self, messages: list[LLMMessage]) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=self._messages_to_input(messages),
        )
        return response.output_text

    def _stream_via_responses(self, messages: list[LLMMessage]) -> Iterator[str]:
        stream = self.client.responses.create(
            model=self.model,
            input=self._messages_to_input(messages),
            stream=True,
        )
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta

    @staticmethod
    def _messages_to_input(messages: list[LLMMessage]) -> list[dict]:
        converted = []
        for message in messages:
            converted.append(
                {
                    "role": message["role"],
                    "content": [{"type": "input_text", "text": message["content"]}],
                }
            )
        return converted
