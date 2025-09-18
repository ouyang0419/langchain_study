# 文档加载器（PDF、Docx、TXT）
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

SUPPORTED_LOADERS = {
    "pdf": PyPDFLoader,
    "docx": Docx2txtLoader,
    # 我们不再直接使用 TextLoader，而是用包装函数
}

# 支持的扩展名
SUPPORTED_EXTENSIONS = ["pdf", "docx", "txt"]


def load_document(file_path: str, file_type: str):
    """
    根据文件类型加载文档，自动处理编码问题
    """
    if file_type.lower() == "txt":
        # ✅ 重点：显式指定 UTF-8 编码
        loader = TextLoader(file_path, encoding="utf-8")
        return loader.load()

    elif file_type.lower() == "pdf":
        loader = PyPDFLoader(file_path)
        return loader.load()

    elif file_type.lower() in ["docx", "doc"]:
        loader = Docx2txtLoader(file_path)
        return loader.load()

    else:
        raise ValueError(f"不支持的文件类型: {file_type}")