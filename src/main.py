from services import simple_search
from utils import load_excel
from views import generate_main_page
import json

def main() -> None:
    print("ЗАПУСК МОДУЛЯ ЛИЧНЫХ ФИНАНСОВ\n")
    test_date = "31.12.2021"
    print(f"Генерация данных для Главной страницы на дату {test_date}...")
    try:
        main_page_data = generate_main_page(test_date)
        print("Результат Главной страницы (JSON):")
        print(json.dumps(main_page_data, ensure_ascii=False, indent=4))
    except Exception as e:
        print(f"Ошибка при генерации главной страницы: {e}")
    print("\n" + "=" * 50 + "\n")
    print("Тестирование сервиса 'Простой поиск'...")
    try:
        all_operations = load_excel()
        search_query = "Каршеринг"
        search_results = simple_search(all_operations, search_query)
        print(f"Найдено операций по запросу '{search_query}': {len(search_results)}")
        if search_results:
            print(f"Пример первой найденной операции:")
            print(json.dumps(search_results[0], ensure_ascii=False, indent=4))
    except Exception as e:
        print(f"Ошибка при выполнении поиска: {e}")


if __name__ == "__main__":
    main()
