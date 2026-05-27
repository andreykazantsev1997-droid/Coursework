from src.services import simple_search


def test_simple_search_success():
    mock_operations = [
        {"Категория": "Каршеринг", "Описание": "Поездка в Яндекс.Драйв", "Сумма": -350},
        {"Категория": "Супермаркеты", "Описание": "Покупка продуктов", "Сумма": -1200},
        {"Категория": "Транспорт", "Описание": "Оплата каршеринга Делимобиль", "Сумма": -200},
    ]
    result_1 = simple_search(mock_operations, "каршеринг")
    assert len(result_1) == 2  # Должен найти 1-ю и 3-ю операции
    result_2 = simple_search(mock_operations, "ПОКУПКА")
    assert len(result_2) == 1
    assert result_2[0]["Категория"] == "Супермаркеты"


def test_simple_search_empty():
    mock_operations = [{"Категория": "Фастфуд", "Описание": "Бургер Кинг"}]
    assert simple_search(mock_operations, "") == []
    assert simple_search(mock_operations, None) == []
