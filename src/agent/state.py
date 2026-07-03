from typing import Any, TypedDict


class CustomerServiceState(TypedDict, total=False):
    history: list[dict[str, str]]
    user_query: str
    knowledge_base_ids: list[str]
    platform: str
    model_name: str
    should_retrieve: bool
    retrieved_chunks: list[dict[str, Any]]
    answer: str
