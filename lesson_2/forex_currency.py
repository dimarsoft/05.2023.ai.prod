from datetime import date

from flask import Flask, render_template, request

from forex_python import converter as fx_converter
from forex_python.converter import RatesNotAvailableError
from currency_converter import CurrencyConverter, RateNotFoundError

app = Flask(__name__, template_folder='templates')

Hundred = 100.0


@app.route('/forex')
def view_forex():
    converter = fx_converter

    today = date.today()

    try:
        course = converter.convert(Hundred, 'EUR', 'USD')

        txt = f'Сегодня {today} за 1 евро дают: {int(course / Hundred)} долларов ' \
              f'{int(course % Hundred)} центов'
    except RatesNotAvailableError as ex:
        print(f"not ready error: {ex}")

        txt = f"Сегодня {today} сервис не доступен"

    return txt


@app.route('/')
def view_main():
    converter = CurrencyConverter()

    currencies = sorted(converter.currencies)

    return render_template("index.html", currencies=currencies)


@app.route('/currency')
def view_currency():
    converter = CurrencyConverter()

    today = date.today()

    try:
        course = converter.convert(Hundred, 'EUR', 'USD')

        txt = f'Сегодня {today} за 1 евро дают: ' \
              f'{int(course / Hundred)} долларов {int(course % Hundred)} центов'

    except RatesNotAvailableError as ex:
        print(f"not ready error: {ex}")

        txt = f"Сегодня {today} сервис не доступен"

    return txt


@app.route('/convert', methods=['POST', 'GET'])
def view_convert():
    from_select = request.args.get('fromSelect', 'EUR')
    to_select = request.args.get('toSelect', 'USD')

    print(f"from_select = {from_select}, to_select = {to_select}")

    converter = CurrencyConverter()

    today = date.today()

    value = 100.0

    try:
        course = converter.convert(value, from_select, to_select)

        txt = f'Сегодня {today} за {value} {from_select} дают: ' \
              f'{course} {to_select} '

    except RatesNotAvailableError as ex:
        print(f"not ready error: {ex}")

        txt = f"Сегодня {today} сервис не доступен"
    except RateNotFoundError as ex:
        print(f"not ready error: {ex}")

        txt = f"Сегодня {today} из {from_select} в {to_select} не узнать, {ex}"

    return txt


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)
