from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    debug: bool = Field(default=False, alias="DEBUG")


class DbConfig(BaseConfig):
    db_host: str = Field(alias="DB_HOST")
    db_port: int = Field(alias="DB_PORT")
    db_user: str = Field(alias="DB_USER")
    db_password: str = Field(alias="DB_PASSWORD")
    db_name: str = Field(alias="DB_NAME")

    db_host_test: str = Field(alias="DB_HOST_TEST")
    db_port_test: int = Field(alias="DB_PORT_TEST")
    db_user_test: str = Field(alias="DB_USER_TEST")
    db_password_test: str = Field(alias="DB_PASSWORD_TEST")
    db_name_test: str = Field(alias="DB_NAME_TEST")

    @property
    def url(self) -> str:
        if self.debug:
            return f"postgresql+asyncpg://{self.db_user_test}:{self.db_password_test}@{self.db_host_test}:{self.db_port_test}/{self.db_name_test}"
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class RedisConfig(BaseConfig):
    redis_url: str = Field(alias="REDIS_URL")
    redis_url_test: str = Field(alias="REDIS_URL_TEST")

    @property
    def url(self) -> str:
        if self.debug:
            return self.redis_url_test
        return self.redis_url


class ApiConfig(BaseConfig):
    api_v1_prefix: str = Field(alias="API_V1_PREFIX")
    base_url: str = Field(alias="BASE_URL")


class Config(BaseConfig):
    db: DbConfig = DbConfig()
    redis: RedisConfig = RedisConfig()
    api: ApiConfig = ApiConfig()


config = Config()
