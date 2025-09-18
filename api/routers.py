from fastapi import APIRouter
from api.endpoints import query, upload

router = APIRouter()
router.include_router(query.router, tags=["rag"])
router.include_router(upload.router, tags=["document"])