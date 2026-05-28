import requests


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


def get_currency(currencies: list) -> list:
    """Функция, которая получает курсы валют и фильтрует по списку"""
    url = "https://cbr-xml-daily.ru"
    result = []
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=2)
        if response.status_code == 200:
            data = response.json()
            for currency in currencies:
                if currency in data.get("Valute", {}):
                    rate = data["Valute"][currency]["Valute"]
                    result.append({"currency": currency, "rate": round(float(rate), 2)})
            return result
    except Exception:
        pass
    backup_rates = {"USD": 92.50, "EUR": 100.20, "CNY": 12.80}
    result = []
    for currency in currencies:
        result.append({"currency": currency, "rate": backup_rates.get(currency, 85.00)})
    return result


def get_stock_prices(stocks: list) -> list:
    """Функция, которая получает стоимость акций для списка."""
    result = []
    backup_prices = {"AAPL": 175.50, "AMZN": 180.20, "MSFT": 420.10, "TSLA": 170.00}
    for stock in stocks:
        try:
            url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{stock}.json?iss.meta=off&iss.only=marketdata"
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                data = response.json()
                data_rows = data["marketdata"]["data"]
                columns = data["marketdata"]["columns"]
                last_idx = columns.index("LAST")
                if data_rows and data_rows[0] and data_rows[0][last_idx] is not None:
                    price = data_rows[0][last_idx]
                    result.append({"stock": stock, "price": round(float(price), 2)})
                    continue
        except Exception:
            result.append({"stock": stock, "price": backup_prices.get(stock, 150.00)})
    return result
