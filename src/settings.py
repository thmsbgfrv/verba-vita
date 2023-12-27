from pydantic_settings import BaseSettings, SettingsConfigDict


# this can be used for implementing 12-factor envirment and validation of setting and easy access to settings
class Settings(BaseSettings, frozen=True):
    model_config = SettingsConfigDict(env_file=".env")
    VERSION: str
    MONGODB_URL: str
    MONGODB_NAME: str


settings = Settings()
