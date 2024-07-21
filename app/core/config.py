class Settings:
    PROJECT_NAME: str = "embMarks Project"
    VERSION: str = "1.0.0"
    
    # custom database
    # Example：postgresql://username:password@localhost/db_name
    DATABASE_URL: str = "postgresql://advx24:adventurex24@47.237.16.22:5432/advx24"
    
    # embedding database
    MILVUS_HOST: str = "101.43.68.130"
    MILVUS_PORT: int = 19530

    # llm api
    OPENAI_API_KEY: str = "sk-ebtvfmxrlzkiiissxvsfpnfwathbjqplljdpiogqvaumjxyy"
    OPENAI_BASE_URL: str = "https://api.siliconflow.cn/v1"
    OPENAI_LLM_MODEL: str = "deepseek-ai/DeepSeek-V2-Chat"
    # OPENAI_API_KEY: str = "sk-9c4e5d4acac844419a62ade2bedf0cef" 
    # OPENAI_BASE_URL: str = "https://api.deepseek.com"
    # OPENAI_LLM_MODEL: str = "deepseek-chat"
    
    # embedding api
    # EMBEDDING_API_URL: str = "https://api.siliconflow.cn/v1/embeddings"
    # EMBEDDING_API_KEY: str = "sk-ebtvfmxrlzkiiissxvsfpnfwathbjqplljdpiogqvaumjxyy"
    # EMBEDDING_MODEL: str = "BAAI/bge-large-zh-v1.5"
    # EMBEDDING_DIM: int = 1024
    # EMBEDDING_API_WORKER: int = 10
    # EMBEDDING_API_URL: str = "https://burn.hair/v1/embeddings"
    # EMBEDDING_API_KEY: str = "sk-Q51cXo5e4xX3x5du24E5652dB335499aA5Ca14B26d319831"
    # EMBEDDING_MODEL: str = "text-embedding-3-large"
    # EMBEDDING_DIM: str = 3072
    # EMBEDDING_API_WORKER: int = 1
    EMBEDDING_API_URL: str = "https://api.jina.ai/v1/embeddings"
    EMBEDDING_API_KEY: str = "jina_1e1107c129974af9b6384759ad6fbb876dWy5osmR0Q45tDcSxsKxEX1aMfm"
    EMBEDDING_MODEL: str = "jina-embeddings-v2-base-zh"
    EMBEDDING_DIM: int = 768
    EMBEDDING_API_WORKER: int = 10
    
    EMBEDDING_CLEAR_WHEN_START: bool = False
    
settings = Settings()
