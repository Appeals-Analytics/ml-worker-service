from .base import BaseDetector
from .config import ml_settings


class EmotionResult:
    
    def __init__(self, emotion_label: str, emotion_score: float):
        self.emotion_label = emotion_label
        self.emotion_score = emotion_score

class EmotionDetector(BaseDetector):
    
    @property
    def model_name(self) -> str:
        return ml_settings.emotion_model
    
    def detect(self, text: str) -> EmotionResult:
        label, score = self._predict(text)
        return EmotionResult(emotion_label=label.lower(), emotion_score=round(score, 4))


emotion_detector = EmotionDetector()
