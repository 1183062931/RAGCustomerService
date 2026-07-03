from langgraph.config import get_stream_writer


def run_knowledge_base_search(retriever, query: str, knowledge_base_ids: list[str], limit: int = 6):
    writer = get_stream_writer()
    writer(
        {
            "event": "tool_start",
            "tool_name": "knowledge_base_search",
            "message": f"开始检索 {len(knowledge_base_ids)} 个知识库",
        }
    )

    chunks = retriever.search(
        query=query,
        knowledge_base_ids=knowledge_base_ids,
        limit=limit,
    )

    sources = [
        {
            "knowledge_base_name": chunk.knowledge_base_name,
            "document_name": chunk.document_name,
            "score": round(chunk.score, 4),
            "preview": chunk.content[:200],
        }
        for chunk in chunks
    ]
    writer(
        {
            "event": "tool_end",
            "tool_name": "knowledge_base_search",
            "message": f"检索完成，命中 {len(chunks)} 个片段",
        }
    )
    writer({"event": "sources", "sources": sources})
    return [chunk.to_dict() for chunk in chunks]
