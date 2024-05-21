from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    host: str
    user: str
    password: str
    name: str
    debug: bool = True

    @property
    def url(self):
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}/{self.name}"

    model_config = SettingsConfigDict(
        env_prefix="db_", env_file=(".env", ".env.local"), extra="allow"
    )
