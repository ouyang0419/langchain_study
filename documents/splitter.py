# 文本切分逻辑
from langchain_text_splitters import CharacterTextSplitter

from config.core import settings

def get_text_splitter():
    return CharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap
    )