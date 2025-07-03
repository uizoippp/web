from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    SECRET_KEY: str

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+asyncmy://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )
    
    @property
    def secret_key(self) -> str:
        if not self.SECRET_KEY:
            raise ValueError("Secret key is not set in the environment variables.")
        return self.SECRET_KEY

    class Config:
        env_file = ".env"  

settings = Settings()
