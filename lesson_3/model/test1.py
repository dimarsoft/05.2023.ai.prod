# Простая полносвязная сеть
from keras import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam

from lesson_3.model.funcs import train_eval_net


def test1(x_test, y_test, train_datagen, val_datagen, y_scaler):
    model_dense = Sequential()
    model_dense.add(Dense(150, input_shape=x_test.shape[1:], activation='relu'))
    model_dense.add(Flatten())
    model_dense.add(Dense(y_test.shape[1], activation='linear'))

    # Обучение модели 3x50 эпох
    # train_eval_net(model_dense, train_datagen, val_datagen, [(2, Adam(learning_rate=1e-4)),
    #                                                          (2, Adam(learning_rate=1e-5)),
    #                                                          (2, Adam(learning_rate=1e-6))],
    #                x_test, y_test, y_scaler, title='Полносвязная')

    train_eval_net(model_dense, train_datagen, val_datagen, [(20, Adam(learning_rate=1e-4))],
                   x_test, y_test, y_scaler, title='Полносвязная')

    model_dense.save("model_currency.h5")
