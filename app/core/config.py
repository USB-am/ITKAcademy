from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # DATABASE_URL: str = 'postgresql+asyncpg://postgres:postgres@localhost/wallet_db'
    DATABASE_URL: str = 'postgresql+asyncpg://postgres:postgres@wallet_db/wallet_db'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
