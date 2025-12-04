from dataclasses import dataclass, field
from datetime import datetime

from asyncer import asyncify

from schemas import (
  MessageProcessedSchema,
  MessageSchema,
)

from .language import language_detector, LanguageDetector
from .sentiment import sentiment_detector, SentimentDetector
from .emotions import emotion_detector, EmotionDetector
from services.qwen_api.service import qwen_service, QwenService
@dataclass 
class MLPipeline:

    language: LanguageDetector = field(default_factory=lambda: language_detector)
    sentiment: SentimentDetector = field(default_factory=lambda: sentiment_detector)
    emotion: EmotionDetector = field(default_factory=lambda: emotion_detector)
    categories: QwenService = field(default_factory=lambda: qwen_service)
    
    def warmup(self) -> None:
        self.language.warmup()
        self.sentiment.warmup()
        self.emotion.warmup()
    
    def cleanup(self) -> None:
        self.language.cleanup()
        self.sentiment.cleanup()
        self.emotion.cleanup()

    def _run_ml_models(self, text: str):
        return (
            self.language.detect(text),
            self.sentiment.detect(text),
            self.emotion.detect(text),
        )

    async def process(self, message: MessageSchema, source: str = "kafka") -> MessageProcessedSchema:
        text = message.text

        lang_result, sentiment_result, emotion_result = await asyncify(self._run_ml_models)(text)
        categories = await self.categories.classify_categories(text)
        
        now = datetime.now()
        event_date = datetime.isoformat(message.timestamp) if message.timestamp else datetime.isoformat(now)
        
        return MessageProcessedSchema(
            external_id=message.external_id,
            event_date=event_date,
            source=source,
            user_id=message.user_id,
            text=text,
            cleaned_text=text,  # TODO: Add text cleaning
            lang_code=lang_result.lang_code,
            lang_score=lang_result.lang_score,
            sentiment_label=sentiment_result.sentiment_label,
            sentiment_score=sentiment_result.sentiment_score,
            emotion_label=emotion_result.emotion_label,
            emotion_score=emotion_result.emotion_score,
            category_level_1=categories.category_level_1,
            category_level_2=categories.category_level_2,
        )
        

ml_pipeline = MLPipeline()
