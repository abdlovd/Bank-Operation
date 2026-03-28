import json

import pandas as pd

from config import EXCEL
from src.reports import spending_by_category
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def open_json_file(path_to_json: str) -> tuple[list, list]:
    """ Функция принимает на вход path_to_json и возвращает символы """
    symbols = []
    stocks = []
    try:
        with open(path_to_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            symbols = data["user_currencies"]
            stocks = data["user_stocks"]
        logger.debug(f"Открыт файл по адресу {path_to_json}")
        return symbols, stocks
    except Exception as e:
        logger.error(f"Произошла ошибка {e}")
        print(e)
        return []


if __name__ == '__main__':
    # main_info("2018-03-04 12:12:12")
    transaction: pd.DataFrame = pd.read_excel(EXCEL, sheet_name="Отчет по операциям")
    #print(analyse_cashback(transaction, 2018, 3))
    print(spending_by_category(transaction, "Супермаркеты", "04.03.2018"))
