import json

import pandas as pd

from config import EXCEL
from src.reports import spending_by_category
from src.services import analyse_cashback
from src.utils import get_stock



def open_json_file(path_to_json: str) -> tuple[list, list]:
    """ Функция принимает на вход path_to_json и возвращает символы """
    symbols = []
    stocks = []
    with open(path_to_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        symbols = data["user_currencies"]
        stocks = data["user_stocks"]
    return symbols, stocks

# transaction: pd.DataFrame = pd.read_excel(EXCEL, sheet_name="Отчет по операциям")


if __name__ == '__main__':
    # main_info("2018-03-04 12:12:12")
    transaction: pd.DataFrame = pd.read_excel(EXCEL, sheet_name="Отчет по операциям")
    #print(analyse_cashback(transaction, 2018, 3))
    print(spending_by_category(transaction, "Супермаркеты", "04.03.2018"))

