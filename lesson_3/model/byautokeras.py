import autokeras as ak


def find_by_ak(x_data_train, y_data_train, x_data_test, y_data_test):
    model = ak.TimeseriesForecaster(
        # указываем число прогнозируемых значений в будущем
        lookback=2,
        predict_from=1,
        predict_until=10,
        # указываем количество триалов для обучения модели
        max_trials=3,
        # указываем, каким образом модель должна оптимизироваться
        objective='val_loss',
        loss='mse'
    )

    # обучаем модель на обучающих данных
    model.fit(
        # передаем обучающие данные
        x_data_train,
        y_data_train,
        # указываем данные для валидации
        validation_data=(x_data_test, y_data_test),
        epochs=10
    )

    return model
