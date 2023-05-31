import base64
import io
from datetime import datetime, timedelta

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request
from matplotlib import pyplot as plt

from tools import currency
from tools import predict_currency

tseries_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@tseries_router.get("/tseries")
async def get_tseries_page(request: Request):
    # получаем данные за неделю по АПИ
    info = currency.get_week_history()

    next_date = datetime.now().date() + timedelta(days=1)

    # строим график
    x = info["Date"]
    y = info["Currency"]

    plt.plot(x, y)
    plt.xlabel('Дата')
    plt.ylabel('USD/EURO')
    plt.xticks(rotation=90)

    # Save the chart to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the chart image as base64
    chart_image_base64 = base64.b64encode(buffer.getvalue()).decode()

    # получаем предсказание

    predict_v = predict_currency.currency_predict(y.values)

    return templates.TemplateResponse("tseries.html",
                                      {"request": request,
                                       "chart_image": chart_image_base64,
                                       "next_date": next_date,
                                       "predict": predict_v})
