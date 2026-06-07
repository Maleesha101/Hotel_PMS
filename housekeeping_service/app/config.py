from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str
    REDIS_URL: str
    KAFKA_BOOTSTRAP: str
    ENVIRONMENT: str = "dev"
    JWT_PUBLIC_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()