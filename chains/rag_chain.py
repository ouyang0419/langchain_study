# RAG 链：检索 + 生成
from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from models.llms import get_llm
from vectorstore.store import get_vectorstore

# RAG 提示词
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识库助手，请根据以下上下文回答问题，不能回答上下文没有的内容。上下文:{context}"),
    ("user", "{question}")
])

# 定义一个函数，收集document中的内容
def collect_documents(segments):
    text = []
    for segment in segments:
        text.append(segment.page_content)

    return text

def debug_context(x):
    print("retriever 输出的 context 类型:", type(x["context"]))
    print("原始内容：",x)
    return x

def get_rag_chain():
    llm = get_llm()
    retriever = get_vectorstore().as_retriever(search_kwargs={"k": 5})

    return (
        {
            "context": itemgetter("question") | retriever | collect_documents,
            "question": itemgetter("question")
        }
        | RunnableLambda(debug_context)
        | rag_prompt
        | llm
        | StrOutputParser()
    )