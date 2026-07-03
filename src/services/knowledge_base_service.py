from pathlib import Path

from src.config.settings import AppSettings
from src.repositories.document_repository import DocumentRepository
from src.repositories.kb_repository import KnowledgeBaseRepository
from src.rag.ingestion.ingest_service import IngestService
from src.utils.ids import new_id


class KnowledgeBaseService:
    def __init__(
        self,
        settings: AppSettings,
        kb_repository: KnowledgeBaseRepository,
        document_repository: DocumentRepository,
        ingest_service: IngestService,
    ) -> None:
        self.settings = settings
        self.kb_repository = kb_repository
        self.document_repository = document_repository
        self.ingest_service = ingest_service

    def create_knowledge_base(self, name: str, description: str):
        return self.kb_repository.create(name=name, description=description)

    def list_knowledge_bases(self):
        return self.kb_repository.list_all()

    def get_knowledge_base(self, knowledge_base_id: str):
        return self.kb_repository.get_by_id(knowledge_base_id)

    def list_documents(self, knowledge_base_id: str):
        return self.document_repository.list_by_kb(knowledge_base_id)

    def ingest_uploaded_markdown(
        self, knowledge_base_id: str, filename: str, content: bytes
    ):
        suffix = Path(filename).suffix or ".md"
        stored_path = self.settings.uploads_dir / f"{new_id('upload')}{suffix}"
        stored_path.write_bytes(content)
        return self.ingest_service.ingest_markdown(
            knowledge_base_id=knowledge_base_id,
            source_path=stored_path,
            original_filename=filename,
        )
