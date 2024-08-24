from flask import Flask, request, jsonify, make_response
from src.Controllers.WebImageProcessingCtrl import WebImageProcessingCtrl as WebCtrl
from BaseFlask import BaseFlask
from applications.ApplicationEnums import AppNames, AppPorts

class GeosystemFlask(BaseFlask):

    def __init__(self):
        super().__init__(AppNames.GEOSYSTEM)

    def register_routes(self):
        @self.app.post('/imageProcessing')
        def ImageProcessingMobile():
            print("Get request from GeosystemApp")
            webCtrl = WebCtrl()
            response = webCtrl.MediaProcessing(request)
            if response['status'] >= 400: 
                return make_response(response['message'], response['status'])
            else:
                return jsonify(response)

    def run(self):
        return super().run(AppPorts.GEOSYSTEM)