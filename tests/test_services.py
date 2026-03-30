from src.services import analyse_cashback


def test_analyse_cashback(sample_df):
    assert analyse_cashback(sample_df, 2021, 12) == '{\n    "Кафе": 15,\n    "Супермаркеты": 30\n}'