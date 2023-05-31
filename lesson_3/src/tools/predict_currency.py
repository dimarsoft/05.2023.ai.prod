from tensorflow.keras.models import load_model

model_series = None


def currency_predict(rows) -> float:
    """
    Предсказание курса на следующий день
    :param rows: Список из 7 показание за неделю
    :return:
        float: Новое значение
    """
    global model_series
    if model_series is None:
        model_series = load_model('static/currency.h5')

    x_test = [rows.tolist()]

    prediction = model_series.predict(x_test)

    return prediction[0][0]
