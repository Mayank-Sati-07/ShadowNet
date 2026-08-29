import os
from typing import List


class Settings:
    app_version = os.getenv("APP_VERSION", "1.0.0")
    environment = os.getenv("APP_ENV", "development")
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    allowed_origins_raw = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000",
    )

    @property
    def allowed_origins(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins_raw.split(",") if origin.strip()]


settings = Settings()
