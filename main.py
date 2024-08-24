import os
from dotenv import load_dotenv
from applications.factories import FlaskAppFactory
from applications.ApplicationEnums import AppNames

def main():
    # Загрузка переменных окружения из .env файла
    load_dotenv()

    # Получение значения переменной окружения для типа приложения
    app_name = os.getenv('APP_TYPE')

    if not app_name:
        print("Ошибка: Переменная окружения 'APP_TYPE' не установлена.")
        return

    app_name = app_name.upper()

    if app_name not in AppNames.__members__:
        print(f"Ошибка: Неизвестное приложение '{app_name}'.")
        return

    app_factory = FlaskAppFactory()
    app_instance = app_factory.create_app(AppNames[app_name])
    app_instance.run()

if __name__ == '__main__':
    main()
