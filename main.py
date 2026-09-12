import urllib.request
import urllib.error
import os
import importlib
import sys


def ping_service(url):
    """Проверить доступность сервиса по URL.
    Возвращает кортеж: (доступен: bool, код ответа: int).
    """
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ServiceMonitor/1.0)"}
    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request, timeout=5)
        code = response.getcode()
        return True, code
    except urllib.error.HTTPError as e:
        return False, e.code
    except urllib.error.URLError:
        return False, 0
    except Exception:
        return False, 0


def check_service_status(name, url):
    """Проверить и вывести статус одного сервиса."""
    available, code = ping_service(url)
    if available:
        status_text = "Доступен"
    else:
        status_text = "Недоступен"

    print(f"  {name}")
    print(f"    URL: {url}")
    print(f"    Статус: {status_text} (код: {code})")
    print()
    return available


def show_all_services():
    """Вывести статус всех сервисов из папки services/."""
    services_dir = os.path.join(os.path.dirname(__file__), "services")
    print("\n=== Мониторинг сервисов ===\n")

    count = 0
    for filename in sorted(os.listdir(services_dir)):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            module = importlib.import_module(f"services.{module_name}")
            check_service_status(module.name, module.url)
            count += 1

    if count == 0:
        print("  Список сервисов пуст.\n")


def add_service(name, url, description):
    """Добавить новый сервис, создав файл в папке services/."""
    safe_name = name.lower().replace(" ", "_")
    services_dir = os.path.join(os.path.dirname(__file__), "services")
    filepath = os.path.join(services_dir, f"{safe_name}.py")

    if os.path.exists(filepath):
        print(f"  Сервис '{name}' уже существует.")
        return False

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f'name = "{name}"\n')
        f.write(f'url = "{url}"\n')
        f.write(f'description = "{description}"\n')

    print(f"  Сервис '{name}' добавлен.")
    return True


def remove_service(name):
    """Удалить сервис по названию."""
    services_dir = os.path.join(os.path.dirname(__file__), "services")
    safe_name = name.lower().replace(" ", "_")
    filepath = os.path.join(services_dir, f"{safe_name}.py")

    if not os.path.exists(filepath):
        print(f"  Сервис '{name}' не найден.")
        return False

    os.remove(filepath)
    print(f"  Сервис '{name}' удалён.")
    return True


def get_service_choice():
    """Получить номер сервиса от пользователя."""
    services_dir = os.path.join(os.path.dirname(__file__), "services")
    files = sorted([
        f for f in os.listdir(services_dir)
        if f.endswith(".py") and not f.startswith("__")
    ])

    if not files:
        print("  Список сервисов пуст.")
        return None

    print("\nДоступные сервисы:")
    for i, filename in enumerate(files, 1):
        module_name = filename[:-3]
        module = importlib.import_module(f"services.{module_name}")
        print(f"  {i}. {module.name}")

    try:
        choice = int(input("\nВведите номер сервиса: "))
        if 1 <= choice <= len(files):
            return choice - 1
        else:
            print("  Неверный номер.")
            return None
    except ValueError:
        print("  Введите число.")
        return None


def get_filename_by_index(index):
    """Получить имя модуля по индексу."""
    services_dir = os.path.join(os.path.dirname(__file__), "services")
    files = sorted([
        f for f in os.listdir(services_dir)
        if f.endswith(".py") and not f.startswith("__")
    ])
    if 0 <= index < len(files):
        return files[index][:-3]
    return None


def print_menu():
    """Вывести главное меню."""
    print("\n=== ServiceMonitor ===\n")
    print("1. Проверить все сервисы")
    print("2. Проверить сервис выборочно")
    print("3. Добавить сервис")
    print("4. Удалить сервис")
    print("5. Выход\n")


def main():
    """Точка запуска приложения."""
    print("\n=== ServiceMonitor ===")
    print("Добро пожаловать! Загружаем сервисы...\n")

    show_all_services()

    while True:
        print_menu()
        choice = input("Выберите действие: ")

        if choice == "1":
            show_all_services()

        elif choice == "2":
            index = get_service_choice()
            if index is not None:
                module_name = get_filename_by_index(index)
                if module_name:
                    module = importlib.import_module(f"services.{module_name}")
                    print()
                    check_service_status(module.name, module.url)

        elif choice == "3":
            print("\nДобавление нового сервиса:")
            name = input("  Название: ").strip()
            url = input("  URL для проверки: ").strip()
            description = input("  Описание: ").strip()
            if name and url:
                add_service(name, url, description)
            else:
                print("  Название и URL обязательны.")

        elif choice == "4":
            index = get_service_choice()
            if index is not None:
                module_name = get_filename_by_index(index)
                if module_name:
                    module = importlib.import_module(f"services.{module_name}")
                    remove_service(module.name)

        elif choice == "5":
            print("\nДо свидания!")
            break

        else:
            print("\n  Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
