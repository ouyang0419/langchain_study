import asyncio

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from chains.rag_chain import get_rag_chain

router = APIRouter(prefix="/api/kb")

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def ask_question(request: QueryRequest):
    chain = get_rag_chain()
    response = await chain.ainvoke({"question": request.question})
    return {"answer": response}


@router.post("/query/stream")
async def stream_question(request: QueryRequest):
    chain = get_rag_chain()

    async def event_generator():
        try:
            # 使用 async generator 逐步获取输出
            async for chunk in chain.astream({"question": request.question}):
                # 每个 chunk 可能是字符串或包含内容的对象
                content = chunk if isinstance(chunk, str) else str(chunk)

                # 发送 SSE 消息
                yield f"data: {content}\n\n"

                # 可选：控制发送频率，避免过快
                await asyncio.sleep(0.02)

        except Exception as e:
            yield f"data: \n\n"
            yield f"error: {str(e)}\n\n"

    # 返回 StreamingResponse，MIME 类型为 text/event-stream
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )