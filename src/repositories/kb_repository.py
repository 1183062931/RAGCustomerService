import sqlite3
from pathlib import Path

from src.domain.models.knowledge_base import KnowledgeBase
from src.utils.ids import new_id
from src.utils.time import now_iso


class KnowledgeBaseRepository:
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
                CREATE TABLE IF NOT EXISTS knowledge_bases (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT NOT NULL,
                    collection_name TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL
                )
                """
            )

    def create(self, name: str, description: str) -> KnowledgeBase:
        kb_id = new_id("kb")
        kb = KnowledgeBase(
            id=kb_id,
            name=name.strip(),
            description=description.strip(),
            collection_name=f"kb_{kb_id.replace('-', '_')}",
            created_at=now_iso(),
        )
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO knowledge_bases (
                    id, name, description, collection_name, created_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    kb.id,
                    kb.name,
                    kb.description,
                    kb.collection_name,
                    kb.created_at,
                ),
            )
        return kb

    def list_all(self) -> list[KnowledgeBase]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM knowledge_bases ORDER BY created_at DESC"
            ).fetchall()
        return [self._to_model(row) for row in rows]

    def get_by_id(self, knowledge_base_id: str) -> KnowledgeBase | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM knowledge_bases WHERE id = ?",
                (knowledge_base_id,),
            ).fetchone()
        return self._to_model(row) if row else None

    @staticmethod
    def _to_model(row: sqlite3.Row) -> KnowledgeBase:
        return KnowledgeBase(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            collection_name=row["collection_name"],
            created_at=row["created_at"],
        )
