from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )
    es_host: str = Field('http://127.0.0.1:9200', alias='ELASTIC_HOST')
    es_index: str = ...
    es_id_field: str = ...
    es_index_mapping: dict = ...

    redis_host: str = ...
    service_url: str = ...


test_settings = TestSettings()