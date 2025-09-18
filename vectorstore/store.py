from langchain_community.embeddings import DashScopeEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore
from config.core import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_vectorstore(index_name: str = "school-kb"):
    embedding_model = DashScopeEmbeddings(
        model="text-embedding-v3",
        dashscope_api_key=settings.dashscope_api_key
    )

    config = RedisConfig(
        index_name=index_name,
        redis_url="redis://127.0.0.1:6379"
    )

    return RedisVectorStore(embedding_model, config=config)