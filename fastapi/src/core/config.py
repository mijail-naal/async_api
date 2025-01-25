import os
from logging import config as logging_config

from core.logger import LOGGING

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='../env/prod/.env',
        env_file_encoding='utf-8'
    )
    project_name: str = ...
    redis_host: str = Field(9200, alias='REDIS_HOST')
    redis_port: int = Field(6379, alias='REDIS_PORT')
    elastic_protocol: str = Field('http', alias='ELASTIC_PROTOCOL')
    elastic_host: str = Field('127.0.0.1', alias='ELASTIC_HOST')
    elastic_port: int = Field(9200, alias='ELASTIC_PORT')


settings = Settings()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

QUERY_DESC = "Search bar"
QUERY_ALIAS = "query"

SORT_ORDER_DESC = "Ordering. asc - ascending, desc - descending"
SORT_ORDER_ALIAS = "sort_order"

SORT_FIELD_DESC = "Sorting field"
SORT_FIELD_ALIAS = "sort_field"

PAGE_DESC = "Page number"
PAGE_ALIAS = "page"

SIZE_DESC = "Total elements for each page"
SIZE_ALIAS = "size"

GENRE_DESC = "Filter by film genre"
GENRE_ALIAS = "genre_id"

MAX_PAGE_SIZE = 100

MAX_GENRES_SIZE = 50
