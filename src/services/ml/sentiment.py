from .base import BaseDetector
from .config import ml_settings


class SentimentResult:
    
    def __init__(self, sentiment_label: str, sentiment_score: float):
        self.sentiment_label = sentiment_label
        self.sentiment_score = sentiment_score

class SentimentDetector(BaseDetector):
    @property
    def model_name(self) -> str:
        return ml_settings.sentiment_model
    
    def detect(self, text: str) -> SentimentResult:
        label, score = self._predict(text)
        sentiment_label = "_".join(label.lower().split(" "))
        return SentimentResult(sentiment_label=sentiment_label, sentiment_score=round(score, 4))


sentiment_detector = SentimentDetector()
