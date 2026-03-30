import logging
import json
import os

from config import root_dir

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(root_dir, "logs", "open_file.log"), encoding="utf-8")
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
        return [], []
