import json
from typing import Dict, Any

from config import JSON, EXCEL
from src.utils import get_time_for_greeting, get_date, path_and_period, get_card_with_spend, get_top_transaction, \
    get_currency, get_stock



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

    #4. Курс Валют
    currency_rates = get_currency(JSON)

    #5. Стоимость акций из S&P500.
    stock_prices = get_stock(JSON)

    data = {
        "greeting": greeting,
        "cards": cards,
        "top_transaction": top_transaction,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    return json_data





