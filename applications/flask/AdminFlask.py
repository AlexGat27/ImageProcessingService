from flask import Flask, request, jsonify, make_response
from src.Controllers.AppProcessingCtrl import AppProcessingCtrl as AppCtrl
from applications.flask import BaseFlask
from applications.ApplicationEnums import AppNames, AppPorts

class AdminFlask(BaseFlask):

    def __init__(self):
        super().__init__(self, AppNames.ADMIN)

    def register_routes(self):
        @self.app.post('/imageProcessing')
        def ImageProcessingAdmin():
            print('Get request from Application')
            appCtrl = AppCtrl("ImageApp")
            data2send = appCtrl.MediaProcessing(request, True)
            return jsonify(data2send)

        @self.app.post('/videoSplit')
        def SplitVideo():
            print('Get request from Application')
            appCtrl = AppCtrl("VideoApp")
            data2send = appCtrl.SplitVideo(request, False)
            return jsonify(data2send)

    def run(self):
        super().run(AppPorts.ADMIN)