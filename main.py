import os
from dotenv import load_dotenv
from applications.factories import FlaskAppFactory, KafkaAppFactory
from applications.ApplicationEnums import AppNames

def main():
    # Загрузка переменных окружения из .env файла
    load_dotenv()

    # Получение значения переменной окружения для типа приложения
    app_name = os.getenv('APP_TYPE')
    microservice_name = os.getenv('MICROSERVICE_TYPE')

    if not app_name or not microservice_name:
        print("Ошибка: Необходимые переменные окружения не установлены.")
        return

    app_name = app_name.upper()

    if app_name not in AppNames.__members__:
        print(f"Ошибка: Неизвестное приложение '{app_name}'.")
        return

    if (microservice_name == "flask"):
        app_factory = FlaskAppFactory()
    elif (microservice_name == "kafka"):
        app_factory = KafkaAppFactory()
    else:
        print(f"Ошибка: Такого типа микросервисв не существует '{microservice_name}'.")
        return
    
    app_instance = app_factory.create_app(AppNames[app_name])
    app_instance.run()

if __name__ == '__main__':
    main()
