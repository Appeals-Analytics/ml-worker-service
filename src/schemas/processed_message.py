from pydantic import BaseModel, Field
from .category_level_1_enum import CategoryLevel1Enum
from .category_level_2_enum import CategoryLevel2Enum
from .emotion_enum import EmotionEnum
from .sentiment_enum import SentimentEnum
from datetime import datetime
from typing import List


class MessageProcessedSchema(BaseModel):
  """Schema for message response"""

  external_id: str = Field(..., description="External identifier for the message")
  event_date: datetime = Field(..., description="Date when the event occurred")
  source: str = Field(..., description="Source of the message")
  user_id: str = Field(..., description="User identifier")
  text: str = Field(..., description="Original message text")
  cleaned_text: str = Field(..., description="Cleaned/processed message text")

  lang_code: str = Field(..., description="Detected language code")
  lang_score: float = Field(..., description="Language detection confidence score")

  sentiment_label: SentimentEnum = Field(..., description="Sentiment classification label")
  sentiment_score: float = Field(..., description="Sentiment classification confidence score")

  emotion_label: EmotionEnum = Field(..., description="Emotion classification label")
  emotion_score: float = Field(..., description="Emotion classification confidence score")

  category_level_1: CategoryLevel1Enum = Field(..., description="Primary category classification")
  category_level_2: List[CategoryLevel2Enum] = Field(
    ..., description="Secondary category classifications"
  )
  
  content_hash: str = Field(..., description="Content hash for filter unique")
