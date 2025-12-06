from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class QwenAPIConfig(BaseSettings):
  qwen_api_key: SecretStr
  qwen_api_base_url: str
  qwen_model: str

  model_config = SettingsConfigDict(env_file=".env", extra="ignore")


qwen_settings = QwenAPIConfig()
