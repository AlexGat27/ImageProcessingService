from flask import Flask, request, jsonify #Импорт для прослушивания запросов и отправки ответов
from src.Controllers.UnityProcessingCtrl import UnityProcessingCtrl as UnitCtrl #Импорт контроллера
from applications.flask import BaseFlask
from applications.ApplicationEnums import AppNames, AppPorts

class UnityFlask(BaseFlask):

    def __init__(self):
        super().__init__(self, AppNames.UNITY)

    def register_routes(self):
        @self.app.post('/imageProcessing') #Обработка POST запроса на обработку изображений
        def ImageProcessingUnity():
            print("Get request from Unity")
            unitCtrl = UnitCtrl() #Объект контроллера
            data2send = unitCtrl.MediaProcessing(request) #Получение данных для отправки ответа
            return jsonify(data2send)

    def run(self):
        return super().run(AppPorts.UNITY)