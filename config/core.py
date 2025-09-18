from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # --- API Keys ---
    openai_api_key: str = Field(..., validation_alias="OPENAI_API_KEY")
    dashscope_api_key: str = Field(..., validation_alias="DASHSCOPE_API_KEY")

    # --- Database ---
    db_host: str = Field(..., validation_alias="DB_HOST")
    db_port: int = Field(..., validation_alias="DB_PORT")
    db_user: str = Field(..., validation_alias="DB_USER")
    db_password: str = Field(..., validation_alias="DB_PASSWORD")
    db_name: str = Field(..., validation_alias="DB_NAME")

    # --- App ---
    app_host: str = Field("0.0.0.0", validation_alias="APP_HOST")
    app_port: int = Field(8000, validation_alias="APP_PORT")
    environment: str = Field("reload", validation_alias="reload")

    # 动态生成数据库 URL
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    # 新增：知识库相关路径
    upload_folder: str = Field("data/uploads", validation_alias="UPLOAD_FOLDER")
    vector_store_path: str = Field("data/vectors", validation_alias="VECTOR_STORE_PATH")
    chunk_size: int = Field(500, validation_alias="CHUNK_SIZE")
    chunk_overlap: int = Field(50, validation_alias="CHUNK_OVERLAP")


    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "populate_by_name": True  # ✅ 新名字（替代 allow_population_by_field_name）
    }

# ✅ 创建全局实例
settings = Settings()