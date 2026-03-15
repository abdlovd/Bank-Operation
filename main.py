import pandas as pd

from config import EXCEL
from src.reports import spending_by_category
from src.services import analyse_cashback
from src.views import main_info

if __name__ == '__main__':
    main_info("2018-03-04 12:12:12")
    analyse_cashback(EXCEL, 2018, 3)
    transaction: pd.DataFrame = pd.read_excel(EXCEL, sheet_name="Отчет по операциям")
    spending_by_category(transaction, "Супермаркеты", "04.03.2018")
