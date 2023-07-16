from pydantic import BaseSettings, Field


class Settings(BaseSettings):

    server_host: str = Field(default="127.0.0.1")
    server_port: int = Field(default=8080)

    pg_driver: str
    pg_host: str
    pg_port: int
    pg_user: str
    pg_password: str
    pg_db: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
