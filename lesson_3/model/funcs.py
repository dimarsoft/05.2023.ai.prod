# Функция расчета результата прогнозирования сети (предсказания)
import numpy as np
from matplotlib import pyplot as plt


def get_pred(model,  # модель
             x_test, y_test,  # тестовая выборка
             y_scaler):  # масштабирующий объект для y

    # Вычисление и деномализация предсказания
    y_pred_unscaled = y_scaler.inverse_transform(model.predict(x_test))

    # Денормализация верных ответов
    y_test_unscaled = y_scaler.inverse_transform(y_test)

    # Возврат результата предсказания и верные ответы в исходном масштабе
    return y_pred_unscaled, y_test_unscaled


# Функция расчета корреляционного коэффициента Пирсона для двух рядов

def correlate(a, b):
    return np.corrcoef(a, b)[0, 1]


# Функция визуализации результата предсказания сети и верных ответов

def show_predict(y_pred, y_true,  # прогноз данных и исходный ряд
                 start,  # точка ряда, с которой начинается отрисовка графика
                 length,  # количество точек для отрисовки графика
                 title=''):

    # Построение графика по всем каналам данных
    plt.figure(figsize=(22, 6))

    plt.plot(y_pred[start:start + length],
             label=f'{0} Прогноз')
    plt.plot(y_true[start:start + length],
             label=f'{0} Базовый')

    plt.title(title)
    plt.xlabel('Время')
    plt.ylabel('Данные')
    plt.legend()
    plt.show()


# Функция рисования корреляций прогнозного ряда и исходного со смещением

def show_corr(y_pred, y_true,  # прогноз данных и исходный ряд
              back_steps_max=30,  # максимальное количество шагов смещения назад по времени
              chn_list=None,  # список каналов данных для отрисовки (по умолчанию все)
              title=''):  # список имен каналов данных

    y_len = y_true.shape[0]
    steps = range(0, back_steps_max + 1)

    # Построение графика по всем каналам данных
    plt.figure(figsize=(14, 7))

    # for chn in chn_list:
    # Вычисление коэффициентов корреляции базового ряда и предсказания с разным смещением
    cross_corr = [correlate(y_true[:y_len - step], y_pred[step:]) for step in steps]
    # Вычисление коэффициентов автокорреляции базового ряда с разным смещением
    auto_corr = [correlate(y_true[:y_len - step], y_true[step:]) for step in steps]

    plt.plot(cross_corr, label=f'{0} Прогноз')
    plt.plot(auto_corr, label=f'{0} Эталон')

    plt.title(title)

    # Назначение меток шкалы оси x
    plt.xticks(steps)
    plt.xlabel('Шаги смещения')
    plt.ylabel('Коэффициент корреляции')
    plt.legend()
    plt.show()


# Функция визуализации результата работы сети

def eval_net(model,  # модель
             x_test, y_test,  # тестовая выборка
             y_scaler,  # нормировщик выхода
             start=0, length=500, back_steps_max=30,  # параметры отображения графиков
             title=''):
    # Получение денормализованного предсказания и данных базового ряда
    y_pred, y_true = get_pred(model, x_test, y_test, y_scaler)

    # Отрисовка графика сопоставления базового и прогнозного рядов
    # Прогнозный ряд сдвигается на 1 шаг назад, так как предсказание делалось на 1 шаг вперед
    show_predict(y_pred[1:], y_true[:-1], start, length,
                 title=f'{title}: Сопоставление базового и прогнозного рядов')
    # Отрисовка графика корреляционных коэффициентов до заданного максимума шагов смещения
    show_corr(y_pred, y_true, back_steps_max=back_steps_max,
              title=f'{title}: Корреляционные коэффициенты по шагам смещения')


# Функция обучения модели и отрисовки прогресса и оценки результатов

def train_eval_net(model,  # модель
                   train_datagen, val_datagen,  # генераторы обучающей и проверочной выборок
                   epoch_list,  # список эпох в виде [(epochs1, opt1), (epochs2, opt2), ...]
                   x_test, y_test,
                   y_scaler,
                   start=0,
                   length=500,
                   back_steps_max=30,
                   title=''):
    # Отображение сводки модели
    model.summary()

    # Обучение модели в несколько фаз в соответствии со списком epoch_list
    for epochs, opt in epoch_list:
        # Компиляция модели
        model.compile(loss='mse', optimizer=opt)
        # Фаза обучения модели
        print(f'Обучение {epochs} эпох')
        history = model.fit(train_datagen,
                            epochs=epochs,
                            validation_data=val_datagen,
                            verbose=1)

        # Рисование графиков прошедшей фазы обучения
        # fig = plt.figure(figsize=(14, 7))
        # plt.plot(history.history['loss'], label='Ошибка на обучающем наборе')
        # plt.plot(history.history['val_loss'], label='Ошибка на проверочном наборе')
        # plt.title(f'{title}: График прогресса обучения')
        # Указание показывать только целые метки шкалы оси x
        # fig.gca().xaxis.get_major_locator().set_params(integer=True)
        # plt.xlabel('Эпоха обучения')
        # plt.ylabel('Средняя ошибка')
        # plt.legend()
        # plt.show()

        # Рисование графиков оценки результата работы модели после фазы обучения
        # eval_net(model, x_test, y_test, y_scaler, start=start,
        #         length=length, back_steps_max=back_steps_max, title=title)