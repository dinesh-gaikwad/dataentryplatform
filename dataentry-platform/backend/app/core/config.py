from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    APP_NAME: str = "DataEntry Platform"
    APP_VERSION: str = "1.0.0"
    SECRET_KEY: str = "change-me"
    DATABASE_URL: str = "sqlite:///./dataentry.db"

settings = Settings()
