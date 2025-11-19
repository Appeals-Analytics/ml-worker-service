from fastapi import FastAPI
from app.utils import lifespan, setup_cors

app = FastAPI(
  title="ML Worker Service",
  description="Worker service for user inputs analyze service",
  lifespan=lifespan,
  )

setup_cors(app)