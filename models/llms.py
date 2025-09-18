from langchain_openai import ChatOpenAI
from config.core import settings

def get_llm():
    return ChatOpenAI(
        model="qwen-plus",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        openai_api_key=settings.openai_api_key
    )