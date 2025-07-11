from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    s3_bucket_name: str
    pymupdf_license: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
