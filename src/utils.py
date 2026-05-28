import json
import os
import re
from datetime import datetime
from typing import Any, cast
from pathlib import Path

import pandas as pd


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


def extract_phone_number(operation_description: str) -> str | None:
    if not operation_description:
        return None
    match = re.search(r'(?:\+7|8)[\s(-]*\d{3}[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}', operation_description)
    if match:
        found_phone = match.group(0)
        clean_phone = re.sub(r'\D', '', found_phone)
        if clean_phone.startswith('7'):
            clean_phone = '8' + clean_phone[1:]
        return clean_phone
    return None


CURRENT_DIR = Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent
DEFAULT_PATH = BASE_DIR / "data" / "operations.xlsx"

def load_excel(file_path: Path = DEFAULT_PATH) -> list[Any]:
    """Функция, которая читает Excel-файл и возвращает список словарей"""
    if not file_path.exists():
        print(f"Критическая ошибка: Файл {file_path} не найден")
        return []
    try:
        data_frame = pd.read_excel(file_path)
        data_frame = data_frame.replace({pd.NA: None, float("nan"): None})
        return data_frame.to_dict(orient="records")
    except Exception as e:
        print(f"Не удалось открыть Excel-файл: {e}")
        return []


def load_user_settings(file_path: str) -> dict[str, Any]:
    """Функция, которая загружает список валют и акций из настроек пользователя"""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as file:
        return cast(dict[str, Any], json.load(file))


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
        except ValueError:
            continue
        if start_date <= operation_date_obj <= end_date:
            filter_operations.append(operation)
    return filter_operations
