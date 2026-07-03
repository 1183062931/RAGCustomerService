from pathlib import Path

import chromadb


class ChromaRepository:
    def __init__(self, persist_path: Path) -> None:
        # 向量数据库落盘目录来自 settings.chroma_dir，默认是 data/chroma。
        # 如果要更换向量库，例如 Milvus、Qdrant、pgvector，建议保持本类方法签名不变，替换内部实现。
        self.client = chromadb.PersistentClient(path=str(persist_path))

    def get_or_create_collection(self, collection_name: str):
        return self.client.get_or_create_collection(name=collection_name)

    def upsert_documents(
        self,
        collection_name: str,
        ids: list[str],
        documents: list[str],
        metadatas: list[dict],
        embeddings: list[list[float]],
    ) -> None:
        collection = self.get_or_create_collection(collection_name)
        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def query(
        self, collection_name: str, query_embedding: list[float], top_k: int = 6
    ) -> list[dict]:
        collection = self.get_or_create_collection(collection_name)
        # Chroma 返回 distance，业务层会转换成 score；不同向量库的距离含义不同，替换库时要同步校准。
        response = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        ids = response.get("ids", [[]])[0]
        documents = response.get("documents", [[]])[0]
        metadatas = response.get("metadatas", [[]])[0]
        distances = response.get("distances", [[]])[0]

        results = []
        for item_id, document, metadata, distance in zip(
            ids, documents, metadatas, distances, strict=False
        ):
            results.append(
                {
                    "id": item_id,
                    "document": document,
                    "metadata": metadata or {},
                    "distance": distance,
                }
            )
        return results
