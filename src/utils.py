import os
import pandas as pd

def load_excel(file_path="../data/operations.xlsx"):
    """Функция, которая читает Excel-файл и возвращает список словарей"""
    if not os.path.exists(file_path):
        print(f"Критическая ошибка: Файл {file_path} не найден")
        return []
    try:
        data_frame = pd.read_excel(file_path)
        data_frame = data_frame.where(pd.notnull(data_frame), None)
        return data_frame.to_dict(orient="records")
    except Exception as e:
        print(f"Не удалось открыть Excel-файл: {e}")
        return []
