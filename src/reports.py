from typing import Optional

import pandas as pd

def file_wrapper(arg):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if arg is not None:
                filename = arg
            else:
                pass


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None):
    df = pd.read_excel(transactions, sheet_name="Отчет по операциям")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    if date is not None:
        given_date = pd.to_datetime(date)
    else:
        given_date= pd.Timestamp.now()

    end_date = given_date
    start_date = given_date - pd.Timedelta(months=3)

    filtered_data: pd.DataFrame = df[
        (df["Категория"] == category)
        &
        (start_date <= df["Дата операции"] >= end_date)
    ]
    return filtered_data
