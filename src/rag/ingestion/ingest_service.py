from pathlib import Path

from src.config.settings import AppSettings
from src.domain.enums import DocumentStatus
from src.rag.loaders.markdown_loader import load_markdown
from src.rag.splitters.markdown_splitter import split_markdown
from src.repositories.chroma_repository import ChromaRepository
from src.repositories.document_repository import DocumentRepository
from src.repositories.kb_repository import KnowledgeBaseRepository
from src.utils.ids import new_id


class IngestService:
    def __init__(
        self,
        settings: AppSettings,
        document_repository: DocumentRepository,
        kb_repository: KnowledgeBaseRepository,
        chroma_repository: ChromaRepository,
        embedding_provider,
    ) -> None:
        self.settings = settings
        self.document_repository = document_repository
        self.kb_repository = kb_repository
        self.chroma_repository = chroma_repository
        self.embedding_provider = embedding_provider

    def ingest_markdown(
        self,
        knowledge_base_id: str,
        source_path: Path,
        original_filename: str,
    ):
        document = self.document_repository.create(
            knowledge_base_id=knowledge_base_id,
            filename=original_filename,
            source_path=str(source_path),
            status=DocumentStatus.PROCESSING,
        )
        try:
            kb = self.kb_repository.get_by_id(knowledge_base_id)
            if kb is None:
                raise ValueError("Knowledge base not found")

            raw_text = load_markdown(source_path)
            # 入库主流程：Markdown 原文先按标题和长度切片，再对每个片段做向量化。
            # 如果要替换切片算法、增加清洗规则或按问答对切分，优先改 split_markdown。
            chunks = split_markdown(
                raw_text,
                chunk_size=self.settings.chunk_size,
                chunk_overlap=self.settings.chunk_overlap,
            )
            if not chunks:
                raise ValueError("No readable content found in markdown file")

            contents = [chunk.content for chunk in chunks]
            # 向量化入口：Embedding 模型必须和检索时使用的模型一致，否则相似度会失真。
            embeddings = self.embedding_provider.embed_documents(contents)

            ids = [new_id("chunk") for _ in chunks]
            metadatas = [
                {
                    "knowledge_base_id": knowledge_base_id,
                    "document_id": document.id,
                    "document_name": original_filename,
                    "section_title": chunk.section_title,
                    "chunk_index": chunk.chunk_index,
                }
                for chunk in chunks
            ]

            # Chroma 写入的是：chunk id、原文片段、metadata 和 embedding。
            # metadata 会在检索结果、工具调用过程、来源展示里继续使用。
            self.chroma_repository.upsert_documents(
                collection_name=kb.collection_name,
                ids=ids,
                documents=contents,
                metadatas=metadatas,
                embeddings=embeddings,
            )
            self.document_repository.update_status(
                document_id=document.id,
                status=DocumentStatus.READY,
                chunk_count=len(chunks),
                error_message=None,
            )
        except Exception as exc:
            self.document_repository.update_status(
                document_id=document.id,
                status=DocumentStatus.FAILED,
                chunk_count=0,
                error_message=str(exc),
            )
            raise

        return self.document_repository.get_by_id(document.id)
