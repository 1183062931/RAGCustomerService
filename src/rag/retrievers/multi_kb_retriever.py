from src.domain.models.chunk import RetrievedChunk
from src.repositories.chroma_repository import ChromaRepository
from src.repositories.kb_repository import KnowledgeBaseRepository


class MultiKnowledgeBaseRetriever:
    def __init__(
        self,
        kb_repository: KnowledgeBaseRepository,
        chroma_repository: ChromaRepository,
        embedding_provider,
        top_k_per_kb: int = 6,
    ) -> None:
        self.kb_repository = kb_repository
        self.chroma_repository = chroma_repository
        self.embedding_provider = embedding_provider
        self.top_k_per_kb = top_k_per_kb

    def search(self, query: str, knowledge_base_ids: list[str], limit: int = 6) -> list[RetrievedChunk]:
        if not knowledge_base_ids:
            return []

        # 检索入口：用户问题必须使用和入库相同的 EmbeddingProvider 转成 query embedding。
        query_embedding = self.embedding_provider.embed_query(query)
        results: list[RetrievedChunk] = []

        for kb_id in knowledge_base_ids:
            kb = self.kb_repository.get_by_id(kb_id)
            if kb is None:
                continue
            matches = self.chroma_repository.query(
                collection_name=kb.collection_name,
                query_embedding=query_embedding,
                top_k=self.top_k_per_kb,
            )
            for match in matches:
                metadata = match["metadata"]
                distance = float(match["distance"])
                # 这里把 Chroma distance 转成越大越相关的 score，方便 UI 和 Agent 统一排序。
                # 如果换成 cosine similarity 或其他向量库，需要重新定义这段归一化逻辑。
                score = 1.0 / (1.0 + distance)
                results.append(
                    RetrievedChunk(
                        chunk_id=match["id"],
                        knowledge_base_id=kb.id,
                        knowledge_base_name=kb.name,
                        document_id=str(metadata.get("document_id", "")),
                        document_name=str(metadata.get("document_name", "")),
                        content=match["document"],
                        score=score,
                        metadata=metadata,
                    )
                )

        results.sort(key=lambda item: item.score, reverse=True)
        return results[:limit]
