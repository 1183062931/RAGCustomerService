from openai import OpenAI

from src.config.settings import AppSettings
from src.rag.embeddings.base import BaseEmbeddingProvider


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, settings: AppSettings) -> None:
        self.api_key = settings.openai_api_key
        client_kwargs = {"api_key": settings.openai_api_key}
        if settings.openai_base_url:
            client_kwargs["base_url"] = settings.openai_base_url
        self.client = OpenAI(**client_kwargs)
        self.model = settings.openai_embedding_model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY 未配置，无法执行向量化。")
        response = self.client.embeddings.create(model=self.model, input=texts)
        return [item.embedding for item in response.data]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]
