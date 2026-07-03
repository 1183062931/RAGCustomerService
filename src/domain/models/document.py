from dataclasses import dataclass


@dataclass(slots=True)
class DocumentRecord:
    id: str
    knowledge_base_id: str
    filename: str
    source_path: str
    status: str
    chunk_count: int
    created_at: str
    error_message: str | None = None
