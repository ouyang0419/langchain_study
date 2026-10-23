# LangChain 学习

个人学习项目。用 FastAPI 搭了一个知识库问答服务，用来练习文档上传、切分、向量检索和 RAG。

这不是线上产品。

## 结构

- `documents`：加载文档，并按配置的长度切分
- `vectorstore`：使用通义千问 `text-embedding-v3` 生成向量，存入本机 Redis
- `chains/rag_chain.py`：先检索，再交给模型生成回答
- `api`：文档上传和问答查询
- `main.py`：FastAPI 入口，提供 `/health`
- `config`：从 `.env` 读取模型密钥、PostgreSQL 连接和切分参数

## 配置

复制 `.env.example` 为 `.env`，填入密钥和数据库连接。`.env` 不要提交到仓库。

向量库默认连接 `redis://127.0.0.1:6379`。
