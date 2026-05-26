from datetime import datetime
from typing import Any, cast
import json
import pandas as pd
import requests

from utils import load_excel


def get_greeting(date_str: str) -> str:
    """Функция, которая возвращает приветствие в зависимости от времени переданной даты/времени."""
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        return "Добрый утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_date_range(date: str) -> tuple[datetime, datetime]:
    """Функция, которая принимает дату и возвращает две даты: Начало месяца и переданная дата."""
    clean_date = date.split()[0]
    end_date = datetime.strptime(clean_date, "%d.%m.%Y")
    start_date = end_date.replace(day=1)
    return start_date, end_date


def filter_operation_by_date(date: str) -> list[dict]:
    """Функция, которая фильтрует операции по диапазону даты"""
    start_date, end_date = get_date_range(date)
    operations = load_excel()
    if isinstance(operations, str):
        operations = json.loads(operations)
    else:
        operations = operations
    filter_operations = []
    for operation in operations:
        operation_date = operation.get("Дата операции")
        if not operation_date:
            continue
        try:
            clean_date = str(operation_date).split()[0]
            operation_date_obj = datetime.strptime(clean_date, "%d.%m.%Y")
        except (ValueError, IndexError):
            continue
        if start_date <= operation_date_obj <= end_date:
            filter_operations.append(operation)
    return filter_operations


# print(filter_operation_by_date("20.05.2020"))


def get_currency(currencies: list) -> list:
    """Функция, которая получает курсы валют и фильтрует по списку"""
    url = "https://cbr-xml-daily.ru"
    result = []
    try:
        response = requests.get(url)
        data = response.json()
        for currency in currencies:
            if currency in data["Valute"]:
                rate = data["Valute"][currency]["Valute"]
                result.append({"currency": currency, "rate": round(float(rate), 2)})
    except (requests.RequestException, KeyError, ValueError):
        print("Ошибка при получении курсов валют.")
    return result


# print(load_user_settings("../user_settings.json"))


def generate_main_page(date_str: str) -> dict[str, Any]:
    """Основная функция для генерации JSON-ответа для главной страницы."""
    filtered_operations = cast(list[dict[str, Any]], filter_operation_by_date(date_str))
    greeting = get_greeting(date_str)
    valid_operations = [op for op in filtered_operations if op.get("Сумма операции") is not None]
    sorted_operations = sorted(
        valid_operations,
        key=lambda x: abs(float(x.get("Сумма операции", 0))),
        reverse=True,
    )
    top_5_transactions = []
    for op in sorted_operations[:5]:
        raw_date = op.get("Дата операции")
        formatted_date = ""
        if raw_date:
            try:
                clean_date = str(raw_date).split()[0]
                dt = datetime.strptime(clean_date, "%d.%m.%Y")
                formatted_date = dt.strftime("%d.%m.%Y")
            except (ValueError, IndexError):
                formatted_date = str(raw_date)
        top_5_transactions.append(
            {
                "date": formatted_date,
                "amount": float(op.get("Сумма операции", 0)),
                "category": op.get("Категория", "Без категории"),
                "description": op.get("Описание", ""),
            }
        )
    response_data = {
        "greeting": greeting,
        "cards": get_cards_info(filtered_operations),
        "top_transactions": top_5_transactions,
        "currency_rates": [],
        "stock_prices": [],
    }
    return response_data


def get_cards_info(operations: list) -> list:
    """Агрегирует данные по картам: расчет расходов и кэшбэка."""
    cards_data = {}
    for op in operations:
        sum_op = op.get("Сумма операции") or op.get("Сумма платежа") or 0
        try:
            sum_op = float(sum_op)
        except (ValueError, TypeError):
            continue
        card_number = op.get("Номер карты") or op.get("Номер Карты")
        if card_number is None or pd.isna(card_number) or str(card_number).lower() == 'nan':
            card_str = "Card"
        else:
            card_str = str(card_number).strip()
        if card_str.endswith('.0'):
            card_str = card_str[:-2]
        card_str = card_str.replace('*', '')
        if not card_str or card_str.lower() == 'nan':
            card_str = "Card"

        if card_str not in cards_data:
            last_digits = card_str[-4:] if len(card_str) >= 4 else "0000"
            cards_data[card_str] = {
                "last_digits": last_digits,
                "total_spent": 0.0,
                "cashback": 0.0
            }
        if sum_op < 0:
            cards_data[card_str]["total_spent"] += abs(sum_op)
        cb = op.get("Кэшбэк") or op.get("Кэшбек") or 0
        try:
            cards_data[card_str]["cashback"] += float(cb)
        except (ValueError, TypeError):
            pass
    result = []
    for card in cards_data.values():
        result.append({
            "last_digits": card["last_digits"],
            "total_spent": round(card["total_spent"]),
            "cashback": round(card["cashback"])
        })
    return result


def get_top_cashback_categories(operations: list) -> list:
    """Возвращает топ-3 категории с наибольшим кэшбэком."""
    cashback_by_cat: dict[str, float] = {}
    for op in operations:
        category = op.get("Категория") or "Без категории"
        cb = op.get("Кэшбэк") or 0
        try:
            cb_float = float(cb)
            if cb_float > 0:
                cashback_by_cat[category] = cashback_by_cat.get(category, 0.0) + cb_float
        except ValueError:
            continue
    sorted_cats = sorted(cashback_by_cat.items(), key=lambda x: x[1], reverse=True)
    result = []
    for cat, cb_sum in sorted_cats[:3]:
        result.append({"category": cat, "cashback": round(cb_sum)})
    return result
