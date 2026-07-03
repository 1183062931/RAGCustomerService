import sqlite3
from pathlib import Path

from src.domain.models.document import DocumentRecord
from src.utils.ids import new_id
from src.utils.time import now_iso


class DocumentRepository:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    knowledge_base_id TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    source_path TEXT NOT NULL,
                    status TEXT NOT NULL,
                    chunk_count INTEGER NOT NULL DEFAULT 0,
                    error_message TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )

    def create(
        self,
        knowledge_base_id: str,
        filename: str,
        source_path: str,
        status: str,
    ) -> DocumentRecord:
        record = DocumentRecord(
            id=new_id("doc"),
            knowledge_base_id=knowledge_base_id,
            filename=filename,
            source_path=source_path,
            status=status,
            chunk_count=0,
            created_at=now_iso(),
            error_message=None,
        )
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO documents (
                    id, knowledge_base_id, filename, source_path, status,
                    chunk_count, error_message, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.id,
                    record.knowledge_base_id,
                    record.filename,
                    record.source_path,
                    record.status,
                    record.chunk_count,
                    record.error_message,
                    record.created_at,
                ),
            )
        return record

    def update_status(
        self,
        document_id: str,
        status: str,
        chunk_count: int,
        error_message: str | None,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE documents
                SET status = ?, chunk_count = ?, error_message = ?
                WHERE id = ?
                """,
                (status, chunk_count, error_message, document_id),
            )

    def list_by_kb(self, knowledge_base_id: str) -> list[DocumentRecord]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM documents
                WHERE knowledge_base_id = ?
                ORDER BY created_at DESC
                """,
                (knowledge_base_id,),
            ).fetchall()
        return [self._to_model(row) for row in rows]

    def get_by_id(self, document_id: str) -> DocumentRecord | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM documents WHERE id = ?",
                (document_id,),
            ).fetchone()
        return self._to_model(row) if row else None

    @staticmethod
    def _to_model(row: sqlite3.Row) -> DocumentRecord:
        return DocumentRecord(
            id=row["id"],
            knowledge_base_id=row["knowledge_base_id"],
            filename=row["filename"],
            source_path=row["source_path"],
            status=row["status"],
            chunk_count=row["chunk_count"],
            created_at=row["created_at"],
            error_message=row["error_message"],
        )
