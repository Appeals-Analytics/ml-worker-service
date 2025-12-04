from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class MessageSchema(BaseModel):
    text: str = Field(..., min_length=1, description="Текст обращения")
    user_id: Optional[str] = Field(None, description="ID пользователя")
    external_id: Optional[str] = Field(None, description="Внешний ID")
    timestamp: Optional[str] = Field(None, description="Время в ISO 8601")