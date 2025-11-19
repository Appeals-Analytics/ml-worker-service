from fastapi import FastAPI
from services.kafka import kafka_service, kafka_settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
  print("Start")
  
  await kafka_service.start_producer()
  await kafka_service.start_consumer(kafka_settings.topic_in)
  
  yield
  
  await kafka_service.close()
  
  print("End")