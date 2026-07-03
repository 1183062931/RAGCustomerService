from dataclasses import asdict, dataclass


@dataclass(slots=True)
class RetrievedChunk:
    chunk_id: str
    knowledge_base_id: str
    knowledge_base_name: str
    document_id: str
    document_name: str
    content: str
    score: float
    metadata: dict

    def to_dict(self) -> dict:
        return asdict(self)
