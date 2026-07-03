from dataclasses import dataclass


@dataclass(slots=True)
class KnowledgeBase:
    id: str
    name: str
    description: str
    collection_name: str
    created_at: str
