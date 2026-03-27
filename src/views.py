import json

import logging
from config import JSON, EXCEL
from main import open_json_file
from src.utils import get_time_for_greeting, get_date, path_and_period, get_card_with_spend, get_top_transaction, \
    get_currency, get_stock


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)



def main_info(date_time:str)-> str:
    """Набор функций и главная функция, принимающая на вход
    строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    и возвращающая JSON-ответ"""

    date_period = get_date(date_time)
    sorted_df = path_and_period(EXCEL, date_period)

    #1. Приветствие
    greeting = get_time_for_greeting()

    #2. По каждой карте
    cards = get_card_with_spend(sorted_df)

    #3. Топ 5 транзакции по сумме платежа
    top_transaction = get_top_transaction(sorted_df, 5)

    #4. Открытие файла
    symbols, stocks = open_json_file(JSON)

    #4. Курс Валют
    currency_rates = get_currency(symbols)

    #5. Стоимость акций из S&P500.
    stock_prices = get_stock(stocks)

    data = {
        "greeting": greeting,
        "cards": cards,
        "top_transaction": top_transaction,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    return json_data




