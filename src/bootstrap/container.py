from pathlib import Path

from src.agent.graph import CustomerServiceGraph
from src.config.settings import AppSettings
from src.llm.factory import ProviderFactory
from src.rag.embeddings.openai_embedding import OpenAIEmbeddingProvider
from src.rag.embeddings.simple_embedding import SimpleEmbeddingProvider
from src.rag.ingestion.ingest_service import IngestService
from src.rag.retrievers.multi_kb_retriever import MultiKnowledgeBaseRetriever
from src.repositories.chroma_repository import ChromaRepository
from src.repositories.document_repository import DocumentRepository
from src.repositories.kb_repository import KnowledgeBaseRepository
from src.services.chat_service import ChatService
from src.services.knowledge_base_service import KnowledgeBaseService
from src.services.provider_service import ProviderService
from src.services.search_service import SearchService


class ServiceContainer:
    def __init__(self, project_root: Path) -> None:
        self.settings = AppSettings.from_env(project_root)
        self.settings.ensure_directories()

        self.kb_repository = KnowledgeBaseRepository(self.settings.sqlite_path)
        self.document_repository = DocumentRepository(self.settings.sqlite_path)
        self.chroma_repository = ChromaRepository(self.settings.chroma_dir)
        # EmbeddingProvider 是“文本 -> 向量”的统一入口。
        # 切换 OpenAI、本地简易向量或新增其他向量模型时，优先改 _build_embedding_provider。
        self.embedding_provider = self._build_embedding_provider()

        self.ingest_service = IngestService(
            settings=self.settings,
            document_repository=self.document_repository,
            kb_repository=self.kb_repository,
            chroma_repository=self.chroma_repository,
            embedding_provider=self.embedding_provider,
        )

        self.knowledge_base_service = KnowledgeBaseService(
            settings=self.settings,
            kb_repository=self.kb_repository,
            document_repository=self.document_repository,
            ingest_service=self.ingest_service,
        )

        self.provider_factory = ProviderFactory(self.settings)
        self.provider_service = ProviderService(self.settings, self.provider_factory)

        self.multi_kb_retriever = MultiKnowledgeBaseRetriever(
            kb_repository=self.kb_repository,
            chroma_repository=self.chroma_repository,
            embedding_provider=self.embedding_provider,
            top_k_per_kb=self.settings.default_top_k,
        )

        self.agent_graph = CustomerServiceGraph(
            provider_service=self.provider_service,
            retriever=self.multi_kb_retriever,
        )
        self.chat_service = ChatService(self.agent_graph)
        self.search_service = SearchService(self.multi_kb_retriever)

    def _build_embedding_provider(self):
        # EMBEDDING_PROVIDER=simple 仅适合本地演示和断网测试；生产环境建议使用 OpenAI 或其他稳定 embedding 服务。
        if self.settings.embedding_provider.lower() == "simple":
            return SimpleEmbeddingProvider()
        return OpenAIEmbeddingProvider(self.settings)
