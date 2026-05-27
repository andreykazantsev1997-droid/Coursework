from datetime import datetime, timedelta

import pandas as pd


def spending_by_category(operations: list, category: str, date: str) -> list:
    """Функция, которая возвращает операции по заданной категории за определенную дату"""
    if date:
        end_date = datetime.strptime(date, "%d.%m.%Y")
    else:
        end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    report_operations = []
    for operation in operations:
        operation_category = operation.get("Категория")
        if not operation_category or str(operation_category).lower() != category.lower():
            continue
        operation_date = operation.get("Дата операции")
        if not operation_date:
            continue
        try:
            clean_date = str(operation_date).split()[0]
            operation_date = datetime.strptime(clean_date, "%d.%m.%Y")
        except ValueError:
            continue
        if start_date <= operation_date <= end_date:
            report_operations.append(operation)
    return report_operations


def get_cards_info(operations: list) -> list:
    """Агрегирует данные по картам: расчет расходов и кэшбэка."""
    cards_data = {}
    for op in operations:
        sum_op = op.get("Сумма операции") or op.get("Сумма платежа") or 0
        try:
            sum_op = float(sum_op)
        except ValueError:
            continue
        card_number = op.get("Номер карты") or op.get("Номер Карты")
        if card_number is None or pd.isna(card_number) or str(card_number).lower() == "nan":
            card_str = "Card"
        else:
            card_str = str(card_number).strip()
        if card_str.endswith(".0"):
            card_str = card_str[:-2]
        card_str = card_str.replace("*", "")
        if not card_str or card_str.lower() == "nan":
            card_str = "Card"

        if card_str not in cards_data:
            last_digits = card_str[-4:] if len(card_str) >= 4 else "0000"
            cards_data[card_str] = {"last_digits": last_digits, "total_spent": 0.0, "cashback": 0.0}
        if sum_op < 0:
            cards_data[card_str]["total_spent"] += abs(sum_op)
        cb = op.get("Кэшбэк") or op.get("Кэшбек") or 0
        try:
            cards_data[card_str]["cashback"] += float(cb)
        except ValueError:
            pass
    result = []
    for card in cards_data.values():
        result.append(
            {
                "last_digits": card["last_digits"],
                "total_spent": round(float(cards_data[card_str]["total_spent"])),
                "cashback": round(float(cards_data[card_str]["cashback"])),
            }
        )
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
