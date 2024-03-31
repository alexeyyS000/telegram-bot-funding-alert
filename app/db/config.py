from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    host: str = "localhost:5432"
    user: str = "username"
    password: str = "password"
    db_name: str = "database"
    debug: bool = True

    @property
    def url(self):
        return f"postgresql+psycopg://{self.user}:{self.password}@localhost:5432/{self.db_name}"

    model_config = SettingsConfigDict(
        env_prefix="db_", env_file=(".env", ".env.local"), extra="allow"
    )
