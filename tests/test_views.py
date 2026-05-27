from unittest.mock import patch

from src.utils import get_date_range
from src.views import filter_operation_by_date


def test_get_date_range_correct():
    start_date, end_date = get_date_range("24.12.2021")
    assert start_date.strftime("%d.%m.%Y") == "01.12.2021"
    assert end_date.strftime("%d.%m.%Y") == "24.12.2021"


@patch("src.utils.load_excel")
def test_filter_operation_by_date(mock_load_excel):
    mock_load_excel.return_value = [
        {"Дата операции": "05.12.2021 12:00:00", "Категория": "Супермаркеты", "Сумма операции": -500},
        {"Дата операции": "24.12.2021 15:30:00", "Категория": "Каршеринг", "Сумма операции": -300},
        {"Дата операции": "01.01.2022 10:00:00", "Категория": "Фастфуд", "Сумма операции": -150},  # Другой месяц
    ]
    result = filter_operation_by_date("25.12.2021")
    assert len(result) == 2
    assert result[0]["Категория"] == "Супермаркеты"
    assert result[1]["Категория"] == "Каршеринг"
