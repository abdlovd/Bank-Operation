from config import EXCEL
from src.services import analyse_cashback
from src.views import main_info

if __name__ == '__main__':
    #main_info("2018-03-04 12:12:12")
    analyse_cashback(EXCEL, 2018, 3)