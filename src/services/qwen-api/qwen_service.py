from .config import qwen_settings
from typing import Self
from openai import AsyncClient
class QwenService:
  
  prompts_folder = "prompts/"
  
  def __init__(self: Self):
     self.client: AsyncClient = AsyncClient(
       api_key=qwen_settings.qwen_api_key,
       base_url=qwen_settings.qwen_api_base_url,
       timeout=15
     )

  
  def __get_prompt__(self: Self, prompt_name: str) -> str:
    
    with open(f"{self.prompts_folder}{prompt_name}.txt", mode="r", encoding="utf-8") as file:
      
      return file.read()
    
    
  async def generate_response(self: Self, prompt_name: str, message: str):
    
    system_prompt = self.__get_prompt__("system")
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]

    response = await self.client.chat.completions.create(
        model=qwen_settings.qwen_model,
        messages=messages,
        temperature=0.1,
        max_tokens=70,
    )

    print(response.choices[0].message.content.strip())
    
    
qwen_service = QwenService()