from unittest.mock import patch


@patch("src.utils.get_date")
@patch("src.utils.path_and_period")
@patch("src.utils.get_time_for_greeting")
@patch("src.utils.get_card_with_spend")
@patch("src.utils.get_top_transaction")
@patch("src.utils.get_currency")
@patch("src.utils.get_stock")
@patch("main.open_json_file")
def test_main_info(j_file, stock, currency, transaction,
              spending, greeting, period, dates):
    from src.views import main_info
    stock.return_value = 1
    currency.return_value = 2
    j_file.return_value = [],[]
    transaction.return_value = 4
    spending.return_value = 5
    greeting.return_value = 6
    period.return_value = 7
    dates.return_value = 8
    assert main_info("2018-03-04 12:12:12")== ('{\n'
 '    "greeting": 6,\n'
 '    "cards": 5,\n'
 '    "top_transaction": 4,\n'
 '    "currency_rates": 2,\n'
 '    "stock_prices": 1\n'
 '}')