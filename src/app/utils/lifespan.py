from fastapi import FastAPI
from services.kafka import kafka_service, kafka_settings
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
  print("Start")
  
  await kafka_service.start_producer()
  await kafka_service.start_consumer([kafka_settings.topic_in])
  await asyncio.create_task(kafka_service.consume_and_process())
  
  yield
  
  await kafka_service.close()
  
  print("End")