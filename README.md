# RAG Customer Service

基于 `Streamlit + LangGraph + Chroma` 的 RAG 智能客服系统，支持：

- 知识库管理：新建知识库、上传 Markdown 文档、自动切分和向量化
- 智能客服对话：基于多知识库检索回答，支持流式输出
- 模型平台：OpenAI / Ollama / Xinference

## 启动

1. 安装依赖
2. 复制 `.env.example` 为 `.env` 并填写配置
3. 运行：

```bash
streamlit run app.py
```
