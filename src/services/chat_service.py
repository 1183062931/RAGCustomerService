from collections.abc import Iterator

from src.agent.graph import CustomerServiceGraph


class ChatService:
    def __init__(self, agent_graph: CustomerServiceGraph) -> None:
        self.agent_graph = agent_graph

    def stream_reply(
        self,
        history: list[dict[str, str]],
        user_query: str,
        knowledge_base_ids: list[str],
        platform: str,
        model_name: str,
    ) -> Iterator[dict]:
        final_answer = ""
        latest_sources: list[dict] = []

        for part in self.agent_graph.stream(
            history=history,
            user_query=user_query,
            knowledge_base_ids=knowledge_base_ids,
            platform=platform,
            model_name=model_name,
        ):
            if part["type"] != "custom":
                continue

            event = part["data"]
            event_type = event.get("event")

            if event_type == "token":
                final_answer += event.get("token", "")
                yield {"type": "token", "delta": event.get("token", ""), "text": final_answer}
            elif event_type == "sources":
                latest_sources = event.get("sources", [])
                yield {"type": "sources", "sources": latest_sources}
            else:
                yield {"type": "tool", "event": event}

        yield {"type": "done", "answer": final_answer.strip(), "sources": latest_sources}
