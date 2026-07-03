def format_tool_event(event: dict) -> str:
    event_type = event.get("event")
    if event_type == "decision":
        return f"决策: {event.get('message', '')}"
    if event_type == "tool_start":
        return f"工具开始: {event.get('message', '')}"
    if event_type == "tool_end":
        return f"工具结束: {event.get('message', '')}"
    if event_type == "answer_start":
        return "回答生成开始"
    if event_type == "answer_end":
        return "回答生成完成"
    return event.get("message", str(event))
