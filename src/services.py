import pandas as pd
import json
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def analyse_cashback(df: pd.DataFrame, year: int, month: int)-> str:
    """ функцию для анализа выгодности категорий повышенного кешбэка,
    выводит JSON с анализом, сколько на каждой категории можно заработать кешбэка
    """
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filtered_data: pd.DataFrame = df[
        (df["Дата операции"].dt.year == year)
        &
        (df["Дата операции"].dt.month == month)
        &
        (df["Сумма платежа"] < 0)
    ]
    logging.info(f"Фильтрация операции по дате: {filtered_data}")

    expenses_by_category: pd.DataFrame = filtered_data.groupby("Категория")["Сумма платежа"].sum()
    cashback_by_category = abs(expenses_by_category) // 100
    dict_ = cashback_by_category.to_dict()
    logging.info("Кэшбэк успешно рассчитан")

    json_file = json.dumps(dict_, ensure_ascii=False, indent=4)

    return json_file
