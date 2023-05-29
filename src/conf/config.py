from pydantic import BaseSettings


class Settings(BaseSettings):
    uri: str = "postgresql+psycopg2://postgres:567234@localhost:5432/rest_app"
    secret_key: str = "secret"
    algorithm: str = "algorithm"
    mail_username: str = "test@test.ua"
    mail_password: str = "password"
    mail_from: str = "test@test.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"
    redis_host: str = "localhost"
    redis_port: int = 6379
    cloudinary_name: str = "cloudinary_name"
    cloudinary_api_key: str = "cloudinary_api_key"
    cloudinary_api_secret: str = "api_secret"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()