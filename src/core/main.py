from fastapi import FastAPI

from src.intermediates.cors import cors_middleware
from src.routers.index import IndexRouter

app = FastAPI(
  title="Brunch OTN Server",
  version="1.2.0",
  docs_url=None,
  redoc_url=None,
  openapi_url=None,
)

app.middleware("https")(cors_middleware)
app.include_router(IndexRouter.router)

@app.get("/")
async def home():
  return "Hello, Brunch OTN Server"

