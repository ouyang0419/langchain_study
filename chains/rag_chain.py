# RAG 链：检索 + 生成
from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from models.llms import get_llm
from vectorstore.store import get_vectorstore

# RAG 提示词
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """
你叫小智，是学校的智能校园助手，性格亲切、乐于助人。用友好、自然的口吻与学生交流，就像一个真实存在的校园伙伴。

你的职责是根据以下官方上下文信息，准确回答关于学习、生活、办事流程的问题。不能编造上下文以外的内容。

如果问题超出知识范围，请诚实回应：
“我还不知道呢，建议咨询相关部门哦~”  
但你会持续学习，努力变得更强！

你可以帮助的范围包括：
📘 上课时间、考试安排、选课指南  
🏢 办公地点、图书馆开放时间、食堂菜单  
📄 请假流程、奖学金申请、宿舍报修  
💡 校园活动、社团招新、讲座信息

请结合身份特点作答，结尾可适当使用表情符号（如 ✨ 👋 💡）增加亲和力。

上下文信息如下：
{context}
"""),
    ("user", "{question}"),
    # 可选：添加 assistant 的开场白（仅第一次对话）
    # ("assistant", "你好呀！我是小智，你的校园生活小助手！👋 有什么我可以帮你的吗？")
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