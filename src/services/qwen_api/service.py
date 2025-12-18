from .config import qwen_settings
from typing import Self
from openai import AsyncClient, APIConnectionError
from schemas import CategoriesResponse
import json
import logging
import asyncio

logger = logging.getLogger("uvicorn.error")


class QwenService:
  prompts_folder = "prompts/"

  def _get_prompt(self: Self, prompt_name: str) -> str:
    try:
      with open(f"{self.prompts_folder}{prompt_name}.txt", mode="r", encoding="utf-8") as file:
        return file.read()
    except FileNotFoundError:
      logger.error(f"Файл промпта {prompt_name} не найден!")
      return ""

  def _create_client(self, base_url: str = None, api_key: str = None) -> AsyncClient:
    api_key = api_key or qwen_settings.qwen_api_key.get_secret_value()
    base_url = base_url or qwen_settings.qwen_api_base_url
    return AsyncClient(
      api_key=api_key,
      base_url=base_url,
      timeout=30,
      max_retries=1,
    )

  async def generate_response(self: Self, prompt_name: str, message: str):
    system_prompt = self._get_prompt(prompt_name)

    messages = [
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": message},
    ]

    try:
      async with self._create_client() as client:
        response = await client.chat.completions.create(
          model=qwen_settings.qwen_model,
          messages=messages,
          temperature=0.1,
          max_tokens=70,
        )

      data = json.loads(response.choices[0].message.content.strip())
      return CategoriesResponse(**data)

    except Exception as e:
      logger.error(f"Общая ошибка (generate_response): {e}")
      raise e

  async def classify_categories(self: Self, message: str, base_url: str = None, api_key: str = None, model: str = None) -> CategoriesResponse:
    model = model or qwen_settings.qwen_model
    system_prompt = self._get_prompt("system_parse")
    messages = [
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": message},
    ]

    try:
      async with self._create_client(base_url=base_url, api_key=api_key) as client:
        response = await client.chat.completions.parse(
          model=model,
          messages=messages,
          temperature=0.1,
          response_format=CategoriesResponse,
        )
      msg_content = response.choices[0].message

      if msg_content.refusal or not msg_content.parsed:
        return CategoriesResponse()

      return msg_content.parsed

    except Exception as e:
      logger.error(f"Непредвиденная ошибка: {e}")
      return await self._classify_with_openrouter(message)

  async def _classify_with_openrouter(self, message: str) -> CategoriesResponse:
    system_prompt = self._get_prompt("system_parse")
    messages = [
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": message},
    ]

    for attempt in range(3):
      try:
        async with self._create_client(
          base_url=qwen_settings.openrouter_base_url,
          api_key=qwen_settings.openrouter_api_key.get_secret_value()
        ) as client:
          response = await client.chat.completions.parse(
          model=qwen_settings.openrouter_model,
          messages=messages,
          temperature=0.1,
          reasoning_effort="low",
          response_format=CategoriesResponse,
        )
        await asyncio.sleep(15)
        print(response)
        msg_content = response.choices[0].message

        if msg_content.refusal or not msg_content.parsed:
          return CategoriesResponse()

        return msg_content.parsed
      except Exception as e:
        logger.error(f"OpenRouter attempt {attempt + 1}: {e}")
        if attempt < 2:
          await asyncio.sleep(10 ** attempt)
    return CategoriesResponse()


qwen_service = QwenService()
