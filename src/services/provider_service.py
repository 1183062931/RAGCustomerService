from src.config.settings import AppSettings
from src.llm.factory import ProviderFactory


class ProviderService:
    def __init__(self, settings: AppSettings, factory: ProviderFactory) -> None:
        self.settings = settings
        self.factory = factory

    def create_provider(self, platform: str, model_name: str):
        return self.factory.create(platform=platform, model_name=model_name)

    def get_default_model(self, platform: str) -> str:
        platform = platform.lower()
        if platform == "openai":
            return self.settings.openai_model
        if platform == "ollama":
            return self.settings.ollama_model
        if platform == "xinference":
            return self.settings.xinference_model
        raise ValueError(f"Unsupported platform: {platform}")

    @staticmethod
    def list_platforms() -> list[str]:
        return ["openai", "ollama", "xinference"]
