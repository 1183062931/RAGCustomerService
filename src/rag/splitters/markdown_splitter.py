from dataclasses import dataclass


@dataclass(slots=True)
class SplitChunk:
    content: str
    section_title: str
    chunk_index: int


def split_markdown(
    markdown_text: str, chunk_size: int = 1200, chunk_overlap: int = 200
) -> list[SplitChunk]:
    # 当前策略：先用 Markdown 标题划分章节，再在章节内按字符窗口切片。
    # 如果要提升生产效果，可以在这里改为按 token、语义段落、QA 块或递归分隔符切片。
    lines = markdown_text.splitlines()
    sections: list[tuple[str, str]] = []
    current_title = "Introduction"
    current_lines: list[str] = []

    for line in lines:
        if line.lstrip().startswith("#"):
            if current_lines:
                sections.append((current_title, "\n".join(current_lines).strip()))
                current_lines = []
            current_title = line.lstrip("#").strip() or "Untitled Section"
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_title, "\n".join(current_lines).strip()))

    chunks: list[SplitChunk] = []
    chunk_index = 0
    for section_title, section_text in sections:
        if not section_text:
            continue
        start = 0
        while start < len(section_text):
            end = min(len(section_text), start + chunk_size)
            content = section_text[start:end].strip()
            if content:
                chunks.append(
                    SplitChunk(
                        content=content,
                        section_title=section_title,
                        chunk_index=chunk_index,
                    )
                )
                chunk_index += 1
            if end == len(section_text):
                break
            # overlap 保留相邻片段上下文，避免答案刚好跨片段边界时召回不完整。
            start = max(0, end - chunk_overlap)
    return chunks
