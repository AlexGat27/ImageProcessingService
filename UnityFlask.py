from flask import Flask, request, jsonify #Импорт для прослушивания запросов и отправки ответов
from src.Controllers.UnityProcessingCtrl import UnityProcessingCtrl as UnitCtrl #Импорт контроллера

unityApp = Flask("UnityApp") #Создание объекта приложения

@unityApp.post('/imageProcessing') #Обработка POST запроса на обработку изображений
def ImageProcessingUnity():
    print("Get request from Unity")
    unitCtrl = UnitCtrl() #Объект контроллера
    data2send = unitCtrl.MediaProcessing(request) #Получение данных для отправки ответа
    return jsonify(data2send)

if __name__ == '__main__':
    unityApp.run(debug=True, port=6002) #Запуск приложения, прослушивающего порт 6002