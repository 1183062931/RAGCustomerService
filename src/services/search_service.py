class SearchService:
    def __init__(self, retriever) -> None:
        self.retriever = retriever

    def search_similar_content(
        self, query: str, knowledge_base_ids: list[str], limit: int = 5
    ):
        cleaned_query = query.strip()
        if not cleaned_query:
            return []
        return self.retriever.search(
            query=cleaned_query,
            knowledge_base_ids=knowledge_base_ids,
            limit=limit,
        )
