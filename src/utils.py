import json
import os
from typing import Any, cast

import pandas as pd


def load_excel(file_path: str = "../data/operations.xlsx") -> list[Any]:
    """Функция, которая читает Excel-файл и возвращает список словарей"""
    if not os.path.exists(file_path):
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
