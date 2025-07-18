from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    DB: str

    def make_url(self, driver: str) -> str:
        return f"{driver}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"

    @property
    def asyncpg_url(self) -> str:
        return self.make_url(driver="postgresql+asyncpg")


class Settings(BaseSettings):
    DB: DatabaseConfig

    class Config:
        case_sensitive = True
        env_nested_delimiter = "__"
        env_file = ".env"
        extra = "ignore"


def get_settings() -> Settings:
    return Settings()