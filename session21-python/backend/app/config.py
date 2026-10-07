from typing import Optional, Union

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    app_name: str = "TaskBoard API"
    database_url: Optional[str] = None
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "taskboard"
    db_user: str = "taskboard"
    db_password: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def sqlalchemy_url(self) -> Union[str, URL]:
        if self.database_url:
            return self.database_url
        if not self.db_password:
            raise ValueError("Set DATABASE_URL or DB_PASSWORD before starting the API")
        return URL.create(
            "postgresql+psycopg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )


settings = Settings()
