from fastapi import FastAPI

from src.core.config import Config
from src.intermediates.cors import cors_middleware
from src.routers.index import IndexRouter

app = FastAPI(
  title="Brunch OTN Server",
  version=Config.VERSION,
  docs_url=None,
  redoc_url=None,
  openapi_url=None,
)

app.middleware("https")(cors_middleware)
app.include_router(IndexRouter.router)

@app.get("/")
async def home():
  return "Hello, Brunch OTN Server"

@app.get("/health")
async def health():
  return "healthy"

@app.get("/version")
async def version():
  return Config.VERSION

