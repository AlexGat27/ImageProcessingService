from flask import Flask, request, jsonify, make_response
from src.Controllers.WebImageProcessingCtrl import WebImageProcessingCtrl as WebCtrl

geosystemMobileApp = Flask("GeosystemMobileApp")

@geosystemMobileApp.post('/imageProcessing')
def ImageProcessingMobile():
    print("Get request from GeosystemApp")
    webCtrl = WebCtrl()
    response = webCtrl.MediaProcessing(request)
    if response['status'] >= 400: 
        return make_response(response['message'], response['status'])
    else:
        return jsonify(response)

if __name__ == '__main__':
    geosystemMobileApp(debug=True, port=6001)