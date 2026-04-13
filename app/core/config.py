import os

# class Settings(BaseSettings):
#     PROJECT_NAME: str = "Cloud Kitchen API"
#     # Azure integration dynamic port extraction is done at runtime in main.py or startup script.
    
#     # Environment configs
#     DATABASE_URL: str = os.getenv("DATABASE_URL")
    
#     # Security
#     SECRET_KEY: str = os.getenv("SECRET_KEY")
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cloud Kitchen API"

    DATABASE_URL: str
    SECRET_KEY: str

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    # class Config:
    #     case_sensitive = True
    #     env_file = ".env"
    #     extra = "ignore"

settings = Settings()
