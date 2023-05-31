from datetime import timedelta

import keras
import pandas as pd
from keras import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam


def week(df):
    from datetime import datetime

    # Assuming your DataFrame has a column named 'timestamp' containing the timestamps

    # Get the current datetime
    current_datetime = datetime.now()

    # Extract the current day of the week and time
    current_day = current_datetime.weekday()  # Monday is 0 and Sunday is 6
    current_time = current_datetime.time()
    one_week_ago = current_datetime - timedelta(days=17)

    # Filter rows based on the current day and time
    filtered_df = df[
        (df['date_datetime'] >= one_week_ago) & (df['date_datetime'] <= current_datetime)]

    print(filtered_df["USD"])


def my_predict():
    model = keras.models.load_model("model_dense.h5")

    # base_data = pd.read_csv("eurofxref-hist.csv", sep=',')
    base_data = pd.read_csv("C:\\AI\\AutoML\\eurofxref-hist\\eurofxref-hist.csv", sep=',')

    base_data['date_datetime'] = pd.to_datetime(base_data['Date'])

    # week(base_data)

    df_sorted = base_data.sort_values('date_datetime')

    # Retrieve the first 7 rows
    first_7_rows = df_sorted.head(7)

    print(first_7_rows["USD"].values)

    x_test = [[1, 2, 3, 4, 5, 6, 7]]
    x_test = []

    x_test.append(first_7_rows["USD"].to_list())

    pred_y = model.predict(x_test)

    print(pred_y)


my_predict()
