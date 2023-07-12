from pydantic import BaseSettings, Field


class Setting(BaseSettings):

    server_host: str = Field(default="127.0.0.1")
    server_port: int = Field(default=8080)

    database_uri: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
