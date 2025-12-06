from .base import BaseDetector
from .config import ml_settings


class LanguageResult:
  def __init__(self, lang_code: str, lang_score: float):
    self.lang_code = lang_code
    self.lang_score = lang_score


class LanguageDetector(BaseDetector):
  @property
  def model_name(self) -> str:
    return ml_settings.language_model

  def detect(self, text: str) -> LanguageResult:
    label, score = self._predict(text)
    return LanguageResult(lang_code=label, lang_score=round(score, 4))


language_detector = LanguageDetector()
