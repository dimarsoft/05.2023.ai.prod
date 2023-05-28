import numpy as np
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from tensorflow.keras.models import load_model
from fastapi import FastAPI, Request, File, UploadFile
import io
from PIL import Image
from fastapi.responses import StreamingResponse

segment_router = APIRouter()

templates = Jinja2Templates(directory="templates")

model_segment = None


@segment_router.get("/segment")
async def get_segment_page(request: Request):
    return templates.TemplateResponse("segment.html",
                                      {"request": request})


@segment_router.post('/segment_predict')
async def segment_predict(image: UploadFile = File(...)):

    global model_segment

    if model_segment is None:
        model_segment = load_model('static/segment.h5')

    img_or = Image.open(image.file).resize((456, 256))
    img = np.array(img_or)
    processed_image = np.expand_dims(img, axis=0)
    predict = np.argmax(model_segment.predict(processed_image), axis=-1)
    mask = labels_to_rgb(predict[..., None])[0]
    # Создание канала альфа-слоя для изображения
    alpha = Image.fromarray(mask).convert('L').point(lambda x: 0 if x == 0 else 255)
    # alpha.save('result.png')
    # Применение маски к изображению
    result = img_or.copy()
    result.putalpha(alpha)

    # Создание нового изображения и вставка на него оригинального изображения
    # и изображения с наложенной маской
    new_img = Image.new('RGBA', (img_or.width * 2, img_or.height), (0, 0, 0, 0))
    new_img.paste(Image.fromarray(mask), (0, 0))
    new_img.paste(result, (img_or.width, 0))

    buffer_inverted = io.BytesIO()
    new_img.save(buffer_inverted, format="PNG")
    buffer_inverted.seek(0)

    return StreamingResponse(buffer_inverted, media_type="image/png")


def labels_to_rgb(image_list) -> np.ndarray:
    AIRPLANE = (255, 255, 255)  # Самолет (белый)
    BACKGROUND = (0, 0, 0)  # Фон (черный)
    CLASS_LABELS = (AIRPLANE, BACKGROUND)
    result = []
    for y in image_list:
        temp = np.zeros((256, 456, 3), dtype='uint8')
        for i, cl in enumerate(CLASS_LABELS):
            temp[np.where(np.all(y == i, axis=-1))] = CLASS_LABELS[i]
        result.append(temp)
    return np.array(result)
