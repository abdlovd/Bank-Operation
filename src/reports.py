from typing import Optional

import pandas as pd

def file_wrapper(arg: str="report.log"):
    """декоратор для функций-отчетов, который записывает в файл результат,
    который возвращает функция, формирующая отчет."""
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            result: pd.DataFrame = func(*args, **kwargs)
            with open(arg, "a", encoding='utf-8') as f:
                f.write(result.to_json(orient="records", date_format="iso", force_ascii=False))
            return result
        return wrapper
    return my_decorator


@file_wrapper("reports.log")
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None):

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)

    if date is not None:
        given_date = pd.to_datetime(date)
    else:
        given_date= pd.Timestamp.now()

    end_date = given_date
    start_date = given_date - pd.DateOffset(months=3)

    transactions = transactions.fillna(None, inplace=True)

    filtered_data: pd.DataFrame = transactions[
        (transactions["Категория"] == category)
        &
        (transactions["Дата операции"] >= start_date)
        &
        (transactions["Дата операции"] <= end_date)
    ]
    return filtered_data

