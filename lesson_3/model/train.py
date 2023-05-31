import numpy as np
import pandas as pd
from keras.preprocessing.sequence import TimeseriesGenerator
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from lesson_3.model.byautokeras import find_by_ak
from lesson_3.model.test1 import test1

# Задание текстовых меток каналов данных (столбцов)
CHANNEL_NAMES = ['dollar_euro']

# Получение словаря с именами и индексами каналов данных
CHANNEL_INDEX = {name: chan for chan, name in enumerate(CHANNEL_NAMES)}
print(CHANNEL_INDEX)


def draw(data):
    # Отображение исходных данных от точки start и длиной length
    start = 00
    length = 300

    # Задание полотна для графиков - два подграфика один под другим с общей осью x
    fig, ax1 = plt.subplots(1, 1, figsize=(22, 13), sharex=True)

    # Четыре основных канала - open, max, min, close
    # Отрисовка одного канала данных
    # От начальной точки start длиной length
    ax1.plot(data[start:start + length],
             label="0")
    ax1.set_ylabel('Цена, руб')
    ax1.legend()

    # Канал volume (объем)
    # ax2.bar(x=np.arange(length),
    #         height=data[start:start + length],
    #         label='Объем')
    # ax2.set_ylabel('Сделки')
    # ax2.legend()

    plt.xlabel('Время')
    # Регулировка пределов оси x
    plt.xlim(0, length)
    # Указание расположить подграфики плотнее друг к другу
    plt.tight_layout()
    # Фиксация графика
    plt.show()


def split2(data):

    SEQ_LEN = 300  # Длина прошедших данных для анализа
    BATCH_SIZE = 20  # Объем батча для генератора
    TEST_LEN = 3000  # 0  # Объем тестовой выборки
    TRAIN_LEN = data.shape[0] - TEST_LEN  # Объем обучающей выборки

    # Разделение данных на тренировочный и тестовый наборы
    # 2*SEQ_LEN - для разрыва между тренировочными и тестовыми данными
    # варьируемый параметр, страховка от пересечения
    data_train, data_test = data[:TRAIN_LEN], data[TRAIN_LEN + 2 * SEQ_LEN:]

    # Отбор входных данных
    x_data_train, x_data_test = data_train[:], data_test[:]

    # Масштабирование данных
    x_scaler = StandardScaler()
    x_scaler.fit(x_data_train)
    x_data_train = x_scaler.transform(x_data_train)
    x_data_test = x_scaler.transform(x_data_test)

    # Отбор выходных данных
    y_data_train, y_data_test = data_train[:], data_test[:]

    # Масштабирование данных
    y_scaler = StandardScaler()
    y_scaler.fit(y_data_train)
    y_data_train = y_scaler.transform(y_data_train)
    y_data_test = y_scaler.transform(y_data_test)

    # Проверка формы данных
    print(f'Train data: {x_data_train.shape}, {y_data_train.shape}')
    print(f'Test  data: {x_data_test.shape}, {y_data_test.shape}')

    return x_data_train, y_data_train, y_scaler, x_data_test, y_data_test
def split(data):
    # Задание гиперпараметров

    # CHANNEL_X = CHANNEL_NAMES  # Отбор каналов входных данных
    # CHANNEL_Y = ['dollar_euro']  # Отбор каналов данных для предсказания
    SEQ_LEN = 7  # Длина прошедших данных для анализа
    BATCH_SIZE = 20  # Объем батча для генератора
    TEST_LEN = 3000  # 0  # Объем тестовой выборки
    TRAIN_LEN = data.shape[0] - TEST_LEN  # Объем обучающей выборки

    # Формирование списков индексов каналов данных для входных и выходных выборок
    # chn_x = [CHANNEL_INDEX[c] for c in CHANNEL_X]
    # chn_y = [CHANNEL_INDEX[c] for c in CHANNEL_Y]

    # Проверка результата
    # print(chn_x, chn_y)

    # Разделение данных на тренировочный и тестовый наборы
    # 2*SEQ_LEN - для разрыва между тренировочными и тестовыми данными
    # варьируемый параметр, страховка от пересечения
    data_train, data_test = data[:TRAIN_LEN], data[TRAIN_LEN + 2 * SEQ_LEN:]

    # Отбор входных данных
    x_data_train, x_data_test = data_train[:], data_test[:]

    # Масштабирование данных
    x_scaler = StandardScaler()
    x_scaler.fit(x_data_train)
    x_data_train = x_scaler.transform(x_data_train)
    x_data_test = x_scaler.transform(x_data_test)

    # Отбор выходных данных
    y_data_train, y_data_test = data_train[:], data_test[:]

    # Масштабирование данных
    y_scaler = StandardScaler()
    y_scaler.fit(y_data_train)
    y_data_train = y_scaler.transform(y_data_train)
    y_data_test = y_scaler.transform(y_data_test)

    # Проверка формы данных
    print(f'Train data: {x_data_train.shape}, {y_data_train.shape}')
    print(f'Test  data: {x_data_test.shape}, {y_data_test.shape}')

    # Создание генератора для обучения
    train_datagen = TimeseriesGenerator(x_data_train,
                                        y_data_train,
                                        length=SEQ_LEN,
                                        stride=1,
                                        sampling_rate=1,
                                        batch_size=BATCH_SIZE)

    # Аналогичный генератор для валидации при обучении
    val_datagen = TimeseriesGenerator(x_data_test,
                                      y_data_test,
                                      length=SEQ_LEN,
                                      stride=1,
                                      sampling_rate=1,
                                      batch_size=BATCH_SIZE)

    # Проверка формы выдаваемого генератором результата
    print(f'Train batch x: {train_datagen[0][0].shape}, y: {train_datagen[0][1].shape}')

    # Генератор тестовой выборки, генерирует один батч на всю выборку
    test_datagen = TimeseriesGenerator(x_data_test,
                                       y_data_test,
                                       length=SEQ_LEN,
                                       stride=1,
                                       sampling_rate=1,
                                       batch_size=x_data_test.shape[0])

    # Формирование тестовой выборки из генератора
    x_test, y_test = test_datagen[0]

    # Проверка формы тестовой выборки
    print(f'Test x: {x_test.shape}, y: {y_test.shape}')

    return x_test, y_test, y_scaler, train_datagen, val_datagen


def show_gen(x_train, y_train, length=10, batch_size=5):
    # Создание генератора TimeseriesGenerator
    gen = TimeseriesGenerator(x_train,
                              y_train,
                              length=length,
                              sampling_rate=1,
                              stride=1,
                              batch_size=batch_size
                              )

    # Прохождение по элементам генератора (батчам) в цикле и вывод каждого батча
    for i, g in enumerate(gen):
        print('Батч №', i)
        print('x_train:\n', g[0])
        print('y_train:\n', g[1])
        print()
    # https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip


base_data = pd.read_csv("C:\\AI\\AutoML\\eurofxref-hist\\eurofxref-hist.csv", sep=',')
# Вывод первых строк таблицы
print(base_data.head())

dollar_euro_df = pd.DataFrame({'dollar_euro': base_data['USD']})

print(dollar_euro_df.head())

# draw(dollar_euro_df)
x_test, y_test, y_scaler, train_datagen, val_datagen = split(dollar_euro_df)

test1(x_test, y_test, train_datagen, val_datagen, y_scaler)


# find_by_ak(x_test, y_test, train_datagen, val_datagen)
