from datetime import datetime, timedelta

import pandas as pd
import requests
from pandas import DataFrame

from settings import APILAYER_APY_KEY


def get_week_history() -> DataFrame:
    """
    Получить курс за неделю (7 дней)
    :return:
        DataFrame - столбцы Date, Currency

    """

    currency = "USD"

    start_date = datetime.now().date()
    end_date = start_date - timedelta(days=6)

    params = {
        "base": "EUR",
        "symbols": currency
    }

    url = f"https://api.apilayer.com/exchangerates_data/timeseries?start_date={end_date}" \
          f"&end_date={start_date}"

    payload = {}
    headers = {
        "apikey": APILAYER_APY_KEY
    }

    response = requests.request("GET", url, headers=headers, data=payload, params=params)

    if response.status_code == 200:
        # Retrieve the JSON response
        data = response.json()
        rates = data['rates']

        tabl = []
        for key in rates:
            usd = rates[key].get(currency)
            tabl.append([key, usd])

        return pd.DataFrame(tabl, columns=["Date", "Currency"])

    else:
        print("Error:", response.status_code, response)
        return pd.DataFrame(columns=["Date", "Currency"])

