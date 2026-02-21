import pandas as pd
import json


def analyse_cashback(file_path: str, year: int, month: int)-> str:
    """ функцию для анализа выгодности категорий повышенного кешбэка,
    выводит JSON с анализом, сколько на каждой категории можно заработать кешбэка
    """
    df = pd.read_excel(file_path)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filtered_data: pd.DataFrame = df[
        (df["Дата операции"].dt.year == year)
        &
        (df["Дата операции"].dt.month == month)
        &
        (df["Кэшбэк"] > 0)
        &
        (df["Сумма платежа"] < 0)
    ]

    expenses_by_category: pd.DataFrame = filtered_data.groupby("Категория")["Сумма платежа"].sum()
    cashback_by_category = abs(expenses_by_category) // 100
    dict_ = cashback_by_category.to_dict()

    json_file = json.dumps(dict_, ensure_ascii=False, indent=4)

    return json_file



