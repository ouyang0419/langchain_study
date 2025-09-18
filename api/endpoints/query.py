from fastapi import APIRouter
from pydantic import BaseModel
from chains.rag_chain import get_rag_chain

router = APIRouter(prefix="/api/kb")

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def ask_question(request: QueryRequest):
    chain = get_rag_chain()
    response = await chain.ainvoke({"question": request.question})
    return {"answer": response}