from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      extra='allow')

    sqlalchemy_database_url: str = 'postgresql+psycopg2://postgres:567234@localhost:5432/rest_app'
    secret_key: str = 'secret'
    algorithm: str = 'HS256'
    mail_username: str = 'check@gmail.com'
    mail_password: str = '5533'
    mail_from: str = 'test@gmail.com'
    mail_port: int = 5533
    mail_server: str = 'smtp.meta.ua'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str = 'name'
    cloudinary_api_key: str = '65655'
    cloudinary_api_secret: str = 'hhh'


settings = EnvSettings()
