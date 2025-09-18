import os
from fastapi import APIRouter, UploadFile, File

from config.core import settings
from documents.loader import load_document
from documents.splitter import get_text_splitter
from vectorstore.store import get_vectorstore

router = APIRouter(prefix="/api/kb")

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # 保存文件
    upload_path = os.path.join(settings.upload_folder, file.filename)
    with open(upload_path, "wb") as f:
        f.write(await file.read())

    # 处理文档
    docs = load_document(upload_path, file.filename.split(".")[-1])
    splits = get_text_splitter().split_documents(docs)

    # 存入向量库
    vectorstore = get_vectorstore()
    vectorstore.add_documents(splits)

    return {"message": "文档上传并处理成功", "filename": file.filename}