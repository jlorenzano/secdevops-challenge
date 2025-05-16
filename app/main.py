from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router
import os

app = FastAPI()

app.include_router(router)
