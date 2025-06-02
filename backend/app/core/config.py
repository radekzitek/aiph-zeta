from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # The default value will be read from the environment variable
    DATABASE_URL: str
    API_CORS_ORIGINS: List[str] = []
    LOGFIRE_WRITE_TOKEN: str
    LOGFIRE_ENVIRONMENT: str

    class Config:
        # This tells Pydantic to look for a .env file
        env_file = ".env"
        extra = "allow"


# Create a single instance that the rest of your app can import
settings = Settings()
