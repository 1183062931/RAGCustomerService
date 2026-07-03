from src.config.settings import AppSettings
from src.llm.base import BaseChatProvider
from src.llm.ollama_provider import OllamaChatProvider
from src.llm.openai_provider import OpenAICompatibleChatProvider
from src.llm.xinference_provider import XinferenceChatProvider


class ProviderFactory:
    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings

    def create(self, platform: str, model_name: str | None = None) -> BaseChatProvider:
        platform = platform.lower()
        if platform == "openai":
            if not self.settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY 未配置，无法使用 OpenAI 对话模型。")
            return OpenAICompatibleChatProvider(
                model=model_name or self.settings.openai_model,
                api_key=self.settings.openai_api_key,
                base_url=self.settings.openai_base_url,
            )
        if platform == "ollama":
            return OllamaChatProvider(
                model=model_name or self.settings.ollama_model,
                api_key=self.settings.ollama_api_key,
                base_url=self.settings.ollama_base_url,
            )
        if platform == "xinference":
            return XinferenceChatProvider(
                model=model_name or self.settings.xinference_model,
                api_key=self.settings.xinference_api_key,
                base_url=self.settings.xinference_base_url,
            )
        raise ValueError(f"Unsupported platform: {platform}")
