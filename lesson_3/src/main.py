
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from models import download_models

from pages.mnist import mnist_router
from pages.router import router_pages
from pages.segment import segment_router
from pages.tseries import tseries_router

app = FastAPI(title="Занятие №3. Сервер")

app.mount("/static", StaticFiles(directory="static"), name="static")

# скачиваем модели при необходимости
download_models()

# Разрешаем запросы CORS от любого источника
origins = ["*"]  # Для простоты можно разрешить доступ со всех источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_pages)
app.include_router(mnist_router)
app.include_router(segment_router)
app.include_router(tseries_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=5020, reload=True)
