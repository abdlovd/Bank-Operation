import os
from typing import Optional
import logging
import pandas as pd

from config import root_dir

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(root_dir, "logs", "reports.log"), encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def file_wrapper(arg: str="report.log"):
    """декоратор для функций-отчетов, который записывает в файл результат,
     и возвращает функция, формирующая отчет."""
    try:
        def my_decorator(func):
            def wrapper(*args, **kwargs):
                result: pd.DataFrame = func(*args, **kwargs)
                with open(arg, "a", encoding='utf-8') as f:
                    f.write(result.to_json(orient="records", date_format="iso", force_ascii=False))
                return result
            return wrapper
        return my_decorator
    except Exception as e:
        logger.error(f"Произошла ошибка {e}")
        return []


@file_wrapper("reports.log")
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None):
    """Функция принимает на вход: датафрейм с транзакциями,
    название категории, опциональную дату. Функция возвращает траты по заданной
    категории за последние три месяца (от переданной даты)."""

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)

    if date is not None:
        given_date = pd.to_datetime(date, dayfirst=True)
    else:
        given_date= pd.Timestamp.now()

    end_date = given_date
    start_date = given_date - pd.DateOffset(months=3)

    transactions = transactions.fillna(None, inplace=True)

    filtered_data: pd.DataFrame = transactions[
        (transactions["Категория"].astype(str).str.lower() == category.lower())
        &
        (transactions["Дата операции"] >= start_date)
        &
        (transactions["Дата операции"] <= end_date)
    ]
    return filtered_data

