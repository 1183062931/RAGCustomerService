from langgraph.config import get_stream_writer
from langgraph.graph import END, START, StateGraph

from src.agent.prompts.system_prompt import SYSTEM_PROMPT
from src.agent.state import CustomerServiceState
from src.agent.tools.knowledge_base_search import run_knowledge_base_search


class CustomerServiceGraph:
    def __init__(self, provider_service, retriever) -> None:
        self.provider_service = provider_service
        self.retriever = retriever
        self.graph = self._build_graph()

    def _build_graph(self):
        builder = StateGraph(CustomerServiceState)
        builder.add_node("decide", self._decide)
        builder.add_node("retrieve", self._retrieve)
        builder.add_node("answer", self._answer)
        builder.add_edge(START, "decide")
        builder.add_conditional_edges(
            "decide",
            self._route_after_decide,
            {
                "retrieve": "retrieve",
                "answer": "answer",
            },
        )
        builder.add_edge("retrieve", "answer")
        builder.add_edge("answer", END)
        return builder.compile()

    @staticmethod
    def _route_after_decide(state: CustomerServiceState) -> str:
        return "retrieve" if state.get("should_retrieve") else "answer"

    @staticmethod
    def _decide(state: CustomerServiceState) -> dict:
        writer = get_stream_writer()
        should_retrieve = bool(state.get("knowledge_base_ids"))
        writer(
            {
                "event": "decision",
                "message": "已启用知识库检索" if should_retrieve else "未启用知识库，将直接回答",
            }
        )
        return {"should_retrieve": should_retrieve}

    def _retrieve(self, state: CustomerServiceState) -> dict:
        # Agent 工具调用点：这里把用户问题交给知识库检索工具。
        # 如果要增加重写查询、多轮补全、rerank 或混合检索，可以在进入工具前后扩展。
        chunks = run_knowledge_base_search(
            retriever=self.retriever,
            query=state["user_query"],
            knowledge_base_ids=state.get("knowledge_base_ids", []),
            limit=6,
        )
        return {"retrieved_chunks": chunks}

    def _answer(self, state: CustomerServiceState) -> dict:
        writer = get_stream_writer()
        provider = self.provider_service.create_provider(
            platform=state["platform"],
            model_name=state["model_name"],
        )

        context_lines = []
        for index, chunk in enumerate(state.get("retrieved_chunks", []), start=1):
            context_lines.append(
                f"[{index}] 知识库: {chunk['knowledge_base_name']} | 文档: {chunk['document_name']}\n"
                f"{chunk['content']}"
            )

        history = state.get("history", [])[-8:]
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history)

        context_block = "\n\n".join(context_lines) if context_lines else "无可用知识库片段。"
        # RAG 拼接点：检索片段在这里进入大模型上下文。
        # 如果要调整回答风格、引用格式、只允许基于知识库回答等策略，改这里和 SYSTEM_PROMPT。
        user_prompt = (
            f"用户问题：{state['user_query']}\n\n"
            f"检索上下文：\n{context_block}\n\n"
            "请基于以上上下文回答。如果上下文不足，请直接说明。"
        )
        messages.append({"role": "user", "content": user_prompt})

        writer({"event": "answer_start", "message": "开始生成回答"})
        answer_parts: list[str] = []
        for token in provider.stream_chat(messages):
            answer_parts.append(token)
            writer({"event": "token", "token": token})
        answer = "".join(answer_parts).strip()
        writer({"event": "answer_end", "message": "回答生成完成"})
        return {"answer": answer}

    def stream(
        self,
        history: list[dict[str, str]],
        user_query: str,
        knowledge_base_ids: list[str],
        platform: str,
        model_name: str,
    ):
        inputs = {
            "history": history,
            "user_query": user_query,
            "knowledge_base_ids": knowledge_base_ids,
            "platform": platform,
            "model_name": model_name,
        }
        yield from self.graph.stream(
            inputs,
            stream_mode=["updates", "custom"],
            version="v2",
        )
