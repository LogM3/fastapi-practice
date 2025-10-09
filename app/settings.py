from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    JWT_SECRET: str = 'jro2i3'
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1

    DB_DRIVER: str = 'postgresql+asyncpg'
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'postgres'
    DB_HOST: str = '127.0.0.1'
    DB_PORT: str = '5432'
    DB_NAME: str = 'postgres'

    TESTING: bool = False
    TESTING_DB_NAME: str = 'testing'

    @property
    def db_url(self) -> str:
        base_url = (
            f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@'
            f'{self.DB_HOST}:{self.DB_PORT}'
        )
        return (
            f'{base_url}'
            f'/{self.TESTING_DB_NAME if self.TESTING else self.DB_NAME}'
        )


settings: Settings = Settings()
