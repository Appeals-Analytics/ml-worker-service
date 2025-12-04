from pydantic import BaseModel, Field
from typing import List
from .category_level_1_enum import CategoryLevel1Enum
from .category_level_2_enum import CategoryLevel2Enum

class CategoriesResponse(BaseModel):
    category_level_1: CategoryLevel1Enum = Field(default=CategoryLevel1Enum.OTHER, description="Основная категория запроса")
    category_level_2: List[CategoryLevel2Enum] = Field(default=[CategoryLevel2Enum.OTHER], description="Список подкатегорий, минимум одна")