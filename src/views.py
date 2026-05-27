from datetime import datetime
from typing import Any

from src.reports import get_cards_info, get_top_cashback_categories
from src.services import get_currency, get_stock_prices
from src.utils import filter_operation_by_date, get_greeting, load_user_settings


def generate_main_page(date_str: str) -> dict[str, Any]:
    """Основная функция для генерации JSON-ответа для главной страницы."""
    filtered_operations = filter_operation_by_date(date_str)
    valid_operations = [op for op in filtered_operations if op.get("Сумма операции") is not None]
    sorted_operations = sorted(valid_operations, key=lambda x: abs(float(x.get("Сумма операции", 0))), reverse=True)
    top_5_transactions = []
    for op in sorted_operations[:5]:
        raw_date = op.get("Дата операции")
        formatted_date = ""
        if raw_date:
            try:
                clean_date = str(raw_date).split()[0]
                dt = datetime.strptime(clean_date, "%d.%m.%Y")
                formatted_date = dt.strftime("%d.%m.%Y")
            except ValueError:
                formatted_date = str(raw_date)
        top_5_transactions.append(
            {
                "date": formatted_date,
                "amount": float(op.get("Сумма операции", 0)),
                "category": op.get("Категория", "Без категории"),
                "description": op.get("Описание", ""),
            }
        )
    try:
        settings = load_user_settings("user_settings.json")
        user_currencies = settings.get("user_currencies", ["USD", "EUR"])
    except Exception:
        user_currencies = ["USD", "EUR"]
    try:
        user_stocks = settings.get("user_stocks", ["AAPL", "AMZN", "MSFT"])
    except Exception:
        user_stocks = ["AAPL", "AMZN"]
    response_data = {
        "greeting": get_greeting(date_str),
        "cards": get_cards_info(filtered_operations),
        "top_transactions": top_5_transactions,
        "top_cashback_categories": get_top_cashback_categories(filtered_operations),
        "currency_rates": get_currency(user_currencies),
        "stock_prices": get_stock_prices(user_stocks),
    }
    return response_data
