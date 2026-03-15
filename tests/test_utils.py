from unittest.mock import patch


from freezegun import freeze_time
from pandas import Timestamp

from src.utils import get_time_for_greeting, get_date, path_and_period, get_card_with_spend, get_top_transaction


@freeze_time("2026-03-12 13:00:00")
def test_get_time_for_greeting1():
    greeting = "Добрый день"
    assert greeting == get_time_for_greeting()

@freeze_time("2026-03-12 09:00:00")
def test_get_time_for_greeting2():
    greeting = "Доброе утро"
    assert greeting == get_time_for_greeting()

@freeze_time("2026-03-12 19:00:00")
def test_get_time_for_greeting3():
    greeting = "Добрый вечер"
    assert greeting == get_time_for_greeting()

@freeze_time("2026-03-12 22:00:00")
def test_get_time_for_greeting4():
    greeting = "Доброй ночи"
    assert greeting == get_time_for_greeting()

def test_get_date():
    assert get_date("2026-03-12 22:00:00") == ['01.03.2026 00:00:00', '12.03.2026 22:00:00']

@patch("pandas.read_excel")
def test_path_and_period(mock_df, sample_df):
    mock_df.return_value = sample_df
    assert path_and_period("",["31.12.2021 15:44:39", "31.12.2021 16:42:04"]).to_dict() == {'Дата операции': {1: Timestamp('2021-12-31 16:42:04'),
                               2: Timestamp('2021-12-31 16:39:04'),
                               3: Timestamp('2021-12-31 15:44:39')},
                             'Дата платежа': {1: '02.10.2024', 2: '03.10.2024', 3: '01.11.2024'},
                             'Категория': {1: 'Супермаркеты', 2: 'Кафе', 3: 'Супермаркеты'},
                             'Номер карты': {1: '*1111', 2: '*2222', 3: '*3333'},
                             'Описание': {1: 'Пятерочка', 2: 'Кофейня', 3: 'Перекресток'},
                             'Сумма платежа': {1: -200, 2: -300, 3: -400}}

def test_get_card_with_spend(sample_2):
    assert get_card_with_spend(sample_2) == [{'cash_back': 1.0, 'last_digits': '7197', 'total_spends': 160.89},
                                 {'cash_back': 0.0, 'last_digits': '7197', 'total_spends': 64.0},
                                 {'cash_back': 1.0, 'last_digits': '7197', 'total_spends': 118.12},
                                 {'cash_back': 0.0, 'last_digits': '7197', 'total_spends': 78.05},
                                 {'cash_back': 5.0, 'last_digits': '5091', 'total_spends': 564.0}]

def test_get_top_transaction(sample_2, numbers):
    assert get_top_transaction(sample_2, numbers) == [{'amount': '-564.0',
                                'category': 'Различные товары',
                                'date': '02.11.2024',
                                'description': 'Ozon.ru'},
                             {'amount': '-160.89',
                                'category': 'Супермаркеты',
                                'date': '01.10.2024',
                                'description': 'Колхоз'},
                             {'amount': '-118.12',
                                'category': 'Супермаркеты',
                                'date': '03.10.2024',
                                'description': 'Магнит'}]

def test_get_currency():
    pass




