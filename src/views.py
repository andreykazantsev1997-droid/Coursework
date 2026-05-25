from datetime import datetime
from http.client import responses

from utils import load_excel
import json
import os
import requests

def get_date_range(date):
    """Функция, которая принимает дату и возвращает две даты: Начало месяца и переданная дата."""
    end_date = datetime.strptime(date, "%d.%m.%Y")
    start_date = end_date.replace(day=1)
    return start_date, end_date

def filter_operation_by_date(date):
    """Функция, которая фильтрует операции по диапазону даты """
    start_date, end_date = get_date_range(date)
    operations = load_excel()
    filter_operations = []
    for operation in operations:
        operation_date = operation.get("Дата операции")
        if not operation_date:
            continue
        try:
            clean_date = str(operation_date).split()[0]
            operation_date = datetime.strptime(clean_date, "%d.%m.%Y")
        except (ValueError, IndexError):
            continue
        if start_date <= operation_date <=end_date:
            filter_operations.append(operation_date)
    return filter_operations

# print(filter_operation_by_date("20.05.2020"))

def load_user_settings(file_path):
    """Функция, которая загружает список валют и акций из настроек пользователя"""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def get_currency(currencies):
    """Функция, которая получает курсы валют и фильтрует по списку"""
    url = "https://cbr-xml-daily.ru"
    result = []
    try:
        response = requests.get(url)
        data = response.json()
        for currency in currencies:
            if currency in data["Valute"]:
                rate = data["Valute"][currency]["Valute"]
                result.append({"currency": currency, "rate": round(float(rate),2)})
    except (requests.RequestException, KeyError, ValueError):
        print("Ошибка при получении курсов валют.")
    return result

# print(load_user_settings("../user_settings.json"))
