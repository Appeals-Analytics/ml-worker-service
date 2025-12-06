from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class MLSettings(BaseSettings):
  model_config = SettingsConfigDict(env_file=".env", extra="ignore")

  language_model: str = "papluca/xlm-roberta-base-language-detection"
  sentiment_model: str = "Niknik149/sentiment_true_cool"
  emotion_model: str = "forxtears/airline-emotion-classifier"

  models_cache_dir: str = "./cache/models"

  num_threads: int = round(os.cpu_count() * 0.7)
  num_interop_threads: int = 1


ml_settings = MLSettings()
