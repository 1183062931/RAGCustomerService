import html
import re


def highlight_text(text: str, query: str) -> str:
    escaped_text = html.escape(text)
    keywords = _extract_keywords(query)
    if not keywords:
        return escaped_text.replace("\n", "  \n")

    pattern = re.compile(
        "(" + "|".join(re.escape(keyword) for keyword in keywords) + ")",
        flags=re.IGNORECASE,
    )
    highlighted = pattern.sub(
        lambda match: f"<mark>{match.group(0)}</mark>",
        escaped_text,
    )
    return highlighted.replace("\n", "  \n")


def _extract_keywords(query: str) -> list[str]:
    raw_keywords = re.findall(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]{1,8}", query)
    cleaned = []
    seen = set()
    for keyword in raw_keywords:
        token = keyword.strip()
        if len(token) <= 1:
            continue
        lowered = token.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        cleaned.append(token)
    return cleaned
