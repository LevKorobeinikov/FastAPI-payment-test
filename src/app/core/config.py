from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=False,
    )
    project_name: str = 'FastAPI Payment Test'
    api_v1_prefix: str = '/api/v1'
    postgres_server: str = 'localhost'
    postgres_port: int = 5432
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    postgres_db: str = 'app'
    secret_key: str = 'secret_key'
    payment_secret_key: str = 'payment_secret_key'
    access_token_expire_minutes: int = 60
    jwt_algorithm: str = 'HS256'

    @property
    def database_url(self) -> str:
        return (
            'postgresql+asyncpg://'
            f'{self.postgres_user}:{self.postgres_password}'
            f'@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}'
        )


settings = Settings()
