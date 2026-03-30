import os
from datetime import datetime
import pandas as pd
from pandas import DataFrame
import logging
import requests
from dotenv import load_dotenv
from config import root_dir

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(root_dir, "logs", "utils.log"), encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


load_dotenv()


url_stock = "https://www.alphavantage.co/query"


def get_time_for_greeting():
    """ Функция возвращает зависимости от текущего
    времени определяет Приветственное сообщение"""
    time_now = datetime.now()
    if 5 <= time_now.hour <= 12:
        return "Доброе утро"
    elif 12 <= time_now.hour <= 18:
        return "Добрый день"
    elif 18 <= time_now.hour <= 21:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_date(date_time: str) -> list[str]:
    """данные с начала месяца, на который выпадает входящая дата, по входящую дату"""
    dt = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    start_of_month = datetime(dt.year, dt.month, 1)
    return [start_of_month.strftime("%d.%m.%Y %H:%M:%S"), dt.strftime("%d.%m.%Y %H:%M:%S")]


def path_and_period(path_to_file: str, period_time: list) -> DataFrame:
    """ Функция принимает путь к Excel файл, и список дат, и возвращает
    таблицу в заданном периоде
    """
    df = pd.read_excel(path_to_file, sheet_name="Отчет по операциям")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    start_date = datetime.strptime(period_time[0], "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(period_time[1], "%d.%m.%Y %H:%M:%S")

    filtered_df = df[
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= end_date)
        ]

    sorted_df = filtered_df.sort_values(by="Дата операции", ascending=True)
    return sorted_df


def get_card_with_spend(sorted_df: DataFrame) -> list[dict]:
    """Реализуйте набор функций и главную функцию, принимающую на вход строку с датой и временем в формате
            YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ со следующими данными:

            По каждой карте:
            последние 4 цифры карты;
            общая сумма расходов;
            кешбэк (1 рубль на каждые 100 рублей)"""
    card_spent_transaction = []
    card_sorted = sorted_df[[
        "Номер карты",
        "Сумма операции",
        "Сумма операции с округлением"
    ]]
    try:
        for index, row in card_sorted.iterrows():
            if row["Сумма операции"] <= 0:
                last_digit = str(row["Номер карты"]).replace("*", "")
                total_spend = row["Сумма операции с округлением"]
                cash_back = total_spend // 100
                row = {
                    "last_digits": last_digit,
                    "total_spends": total_spend,
                    "cash_back": cash_back
                }
                card_spent_transaction.append(row)
        return card_spent_transaction
    except Exception as e:
        logger.error(f"Произошла ошибка {e}")
        return []


def get_top_transaction(sorted_df: DataFrame, get_top):
    """ Функция принимаем DataFrame и возвращает топ транзакций по сумме платежа."""
    top_pay_transaction = []
    expenses_df = sorted_df[sorted_df["Сумма операции"] < 0]
    sorted_pay_df = expenses_df.sort_values(by="Сумма операции", key=lambda x: x.abs(), ascending=False)
    top_transaction = sorted_pay_df.head(get_top)
    sort_top_transaction = top_transaction[
        [
            "Дата платежа",
            "Сумма операции",
            "Категория",
            "Описание"
        ]
    ]

    for index, row in sort_top_transaction.iterrows():
        transaction = {
            "date": f"{row["Дата платежа"]}",
            "amount": f"{row["Сумма операции"]}",
            "category": f"{row["Категория"]}",
            "description": f"{row["Описание"]}"
        }
        top_pay_transaction.append(transaction)
    return top_pay_transaction

def get_currency(symbols):
    """ Функция принимает символ от Excel файла и возвращает курс валюту """
    symbol = ",".join(symbols)
    base = "RUB"
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbol}&base={base}"
    headers = {"apikey": os.getenv("API_KEY")}
    response = requests.get(url, headers=headers, data={})
    result_cur = []
    try:
        for k, v in response.json().get("rates").items():
            result_cur.append({"currency": k, "rate": round(1/v, 2)})
        return result_cur
    except Exception as e:
        logger.error(f"Произошла ошибка {e}")
        return []

def get_stock(stocks: list) -> list[dict]:
    """Функция принимает символ stocks от Excel файла и возвращает стоимость акций из S&P500."""
    stock_rates = []
    try:
        for stock in stocks:
            params = {
                "symbol": f"{stock}",  "apikey": os.getenv("API_KEY_ALPHA_VINTAGE"), "function": "GLOBAL_QUOTE"
            }

            r = requests.get(url_stock, data={}, params=params)
            status_code = r.status_code
            if status_code == 200:
                result = r.json()
                if "Global Quote" in result:
                    stock_name = result["Global Quote"]["01. symbol"]
                    price = float(result["Global Quote"]["05. price"])
                    stock_rates.append({
                        "stock": stock_name,
                        "price": price
                    })
        return stock_rates
    except Exception as e:
        logger.error(f"Произошла ошибка {e}")
        return []
