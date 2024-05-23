import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )
    project_name: str = ...
    redis_host: str = Field(9200, alias='REDIS_HOST')
    redis_port: int = Field(6379, alias='REDIS_PORT')
    elastic_protocol: str = ...
    elastic_host: str = Field('127.0.0.1', alias='ELASTIC_HOST')
    elastic_port: int = Field(9200, alias='ELASTIC_PORT')
    service_url: str = ...


test_settings = TestSettings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
