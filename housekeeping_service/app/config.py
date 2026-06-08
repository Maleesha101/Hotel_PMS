from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    APP_NAME: str = "housekeeping-service"
    APP_PORT: int = 8082
    ENVIRONMENT: str = "dev"

    # Database (using SQLite for local dev/testing)
    DB_URL: str = "sqlite+aiosqlite:///./test.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6380/0"
    ROOM_STATUS_CHANNEL: str = "hotel:room-status"

    # Kafka
    KAFKA_BOOTSTRAP: str = "localhost:9093"
    KAFKA_CONSUMER_GROUP: str = "housekeeping-service"
    # New topic constants
    TASK_COMPLETED_TOPIC: str = "hotel:task-completed"
    INVENTORY_TX_TOPIC: str = "hotel:inventory-transaction"
    DAMAGE_MAINTENANCE_TOPIC: str = "hotel:damage-to-maintenance"
    DAMAGE_INVOICE_TOPIC: str = "hotel:damage-to-invoice"

    # JWT
    JWT_PUBLIC_KEY: str = ""

    # Scheduler
    LOW_STOCK_CHECK_CRON: str = "0 7 * * *"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
