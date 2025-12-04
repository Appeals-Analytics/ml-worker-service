from fastapi import FastAPI
from services.kafka import kafka_service, kafka_settings
from services.ml import ml_pipeline
from services.qwen_api.service import qwen_service
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
  print("Starting...")
  
  ml_pipeline.warmup()
  
  await kafka_service.start_producer()
  await kafka_service.start_consumer([kafka_settings.topic_in])
  
  asyncio.create_task(kafka_service.consume_and_process())
  
  print("Ready")

  yield
  ml_pipeline.cleanup()

  await kafka_service.close()
  
  print("Shutdown complete")