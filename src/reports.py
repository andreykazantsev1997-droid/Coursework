from datetime import datetime, timedelta


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
        except (ValueError, IndexError):
            continue
        if start_date <= operation_date <= end_date:
            report_operations.append(operation)
    return report_operations
