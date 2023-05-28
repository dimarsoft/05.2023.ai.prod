import io

from PIL import Image
import base64
from typing import Dict

import numpy as np
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from tensorflow.keras.models import load_model

mnist_router = APIRouter()

templates = Jinja2Templates(directory="templates")

model_mnist = None # load_model('static/model_mnist.h5')


@mnist_router.get("/mnist")
async def get_about_page(request: Request):
    return templates.TemplateResponse("mnist.html",
                                      {"request": request})


@mnist_router.post("/mnist_predict")
async def predict(data: Dict[str, str]):
    global model_mnist
    if model_mnist is None:
        model_mnist = load_model('static/model_mnist.h5')
    # Декодируем данные изображения из формата base64
    image_data = base64.b64decode(data['image_data'])
    # Преобразуем данные в объект изображения
    image = Image.open(io.BytesIO(image_data))
    # Преобразуем изображение в массив NumPy и изменяем его размер
    image = image.convert('L').resize((28, 28))
    # Нормализуем значения пикселей изображения
    image = np.array(image) / 255.0
    # Разворачиваем массив в одномерный вектор
    processed_image = np.expand_dims(image.flatten(), axis=0)
    # Используем модель для предсказания цифры
    predictions = model_mnist.predict(processed_image)
    # Получаем номер цифры с наибольшей вероятностью
    digit = np.argmax(predictions)
    # Возвращаем предсказанную цифру
    return {"digit": int(digit)}
