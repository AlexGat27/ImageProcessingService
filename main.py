from flask import Flask, request, jsonify, make_response
import threading
from src.Controllers.UnityProcessingCtrl import UnityProcessingCtrl as UnitCtrl
from src.Controllers.WebImageProcessingCtrl import WebImageProcessingCtrl as WebCtrl
from src.Controllers.AppProcessingCtrl import AppProcessingCtrl as AppCtrl

geosystemMobileApp = Flask("GeosystemMobileApp")
unityApp = Flask("UnityApp")
tkinterApp = Flask("TkinterApp")
portMobile = 6001
portUnity = 6000
portTkinter = 6002

@geosystemMobileApp.post('/imageProcessing')
def ImageProcessingMobile():
    print("Get request from GeosystemApp")
    webCtrl = WebCtrl()
    response = webCtrl.MediaProcessing(request)
    if response['status'] >= 400: 
        return make_response(response['message'], response['status'])
    else:
        return jsonify(response)

@unityApp.post('/imageProcessing')
def ImageProcessingUnity():
    print("Get request from Unity")
    unitCtrl = UnitCtrl()
    data2send = unitCtrl.MediaProcessing(request)
    return jsonify(data2send)

@tkinterApp.post('/imageProcessing')
def ImageProcessingTkinter():
    print('Get request from Application')
    appCtrl = AppCtrl("ImageApp")
    data2send = appCtrl.MediaProcessing(request, True)
    return jsonify(data2send)
    
@tkinterApp.post('/videoProcessing')
def ProcessVideo():
    print('Get request from Application')
    appCtrl = AppCtrl("VideoApp")
    data2send = appCtrl.MediaProcessing(request, False)
    return jsonify(data2send)

@tkinterApp.post('/videoSplit')
def SplitVideo():
    print('Get request from Application')
    appCtrl = AppCtrl("VideoApp")
    data2send = appCtrl.SplitVideo(request, False)
    return jsonify(data2send)

if __name__ == '__main__':
    # thread1 = threading.Thread(target=lambda: geosystemMobileApp.run(debug=True, port=portMobile))
    # thread2 = threading.Thread(target=lambda: unityApp.run(debug=True, port=portUnity))
    # thread3 = threading.Thread(target=lambda: tkinterApp.run(debug=True, port=portTkinter))
    # thread1.start()
    # thread2.start()
    # thread3.start()
    geosystemMobileApp.run(debug=True, port=portMobile)