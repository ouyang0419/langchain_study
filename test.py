from langchain_core.documents import Document

from vectorstore.store import get_vectorstore
segments_documents = [
    Document(
        page_content="美团是一家科技零售公司，通过科技和服务，帮助大家吃得更好，生活更好。",
        metadata={"source": "meituan.pdf", "page": 1, "doc_id": "1"}
    ),
    Document(
        page_content="美团创立于2010年，总部位于北京，业务覆盖餐饮、外卖、酒店、旅游等多个领域。",
        metadata={"source": "meituan.pdf", "page": 2, "doc_id": "1"}
    ),
    Document(
        page_content="深度学习是人工智能的核心技术之一，广泛应用于图像识别、自然语言处理等领域。",
        metadata={"source": "ai.pdf", "page": 1, "doc_id": "2"}
    )
]
vectorstore = get_vectorstore("school-kb")
vectorstore.add_documents(segments_documents)

results = vectorstore.similarity_search("美团是做什么的？")
print(results[0].page_content)