import math
import re

from src.rag.embeddings.base import BaseEmbeddingProvider


class SimpleEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, dimensions: int = 512) -> None:
        self.dimensions = dimensions

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        tokens = self._tokenize(text)
        if not tokens:
            return vector

        for token in tokens:
            index = hash(token) % self.dimensions
            vector[index] += 1.0

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [value / norm for value in vector]

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        normalized = re.sub(r"\s+", " ", text.strip().lower())
        tokens = re.findall(r"[a-z0-9_]+|[\u4e00-\u9fff]", normalized)
        return tokens
