def simple_search(operations: list, search_string: str) -> list:
    """Функция простого поиска в описании и категории транзакции"""
    if not search_string:
        return []
    search_query = str(search_string).lower()
    matched_operations = []
    for operation in operations:
        description = str(operation.get("Описание", "")).lower()
        category = str(operation.get("Категория", "")).lower()
        if search_query in description or search_query in category:
            matched_operations.append(operation)
    return matched_operations
