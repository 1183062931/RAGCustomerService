import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(slots=True)
class AppSettings:
    project_root: Path
    data_dir: Path
    chroma_dir: Path
    uploads_dir: Path
    processed_dir: Path
    sqlite_path: Path
    openai_api_key: str
    openai_base_url: str | None
    openai_model: str
    openai_embedding_model: str
    ollama_base_url: str
    ollama_api_key: str
    ollama_model: str
    xinference_base_url: str
    xinference_api_key: str
    xinference_model: str
    default_chat_platform: str
    embedding_provider: str
    default_top_k: int
    chunk_size: int
    chunk_overlap: int

    @classmethod
    def from_env(cls, project_root: Path) -> "AppSettings":
        load_dotenv(project_root / ".env")
        load_dotenv(project_root / "service.env", override=True)

        data_dir = project_root / "data"
        return cls(
            project_root=project_root,
            data_dir=data_dir,
            chroma_dir=data_dir / "chroma",
            uploads_dir=data_dir / "uploads",
            processed_dir=data_dir / "processed",
            sqlite_path=data_dir / "app.db",
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            openai_base_url=os.getenv("OPENAI_BASE_URL") or None,
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            openai_embedding_model=os.getenv(
                "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
            ),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            ollama_api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
            ollama_model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct"),
            xinference_base_url=os.getenv(
                "XINFERENCE_BASE_URL", "http://localhost:9997/v1"
            ),
            xinference_api_key=os.getenv("XINFERENCE_API_KEY", "EMPTY"),
            xinference_model=os.getenv("XINFERENCE_MODEL", "qwen2.5-instruct"),
            default_chat_platform=os.getenv("DEFAULT_CHAT_PLATFORM", "openai"),
            # AI/RAG 调优入口：这些值直接影响入库切片、检索召回数量和向量化平台。
            # 修改后通常需要重启 Streamlit；已入库文档若要应用新的切片/Embedding，需要重新上传入库。
            embedding_provider=os.getenv("EMBEDDING_PROVIDER", "openai"),
            default_top_k=int(os.getenv("DEFAULT_TOP_K", "6")),
            chunk_size=int(os.getenv("CHUNK_SIZE", "1200")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "200")),
        )

    def ensure_directories(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_dir.mkdir(parents=True, exist_ok=True)
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
