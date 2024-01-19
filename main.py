from flask import Flask, request, jsonify, abort
from src.Controllers.UnityProcessingCtrl import UnityProcessingCtrl as UnitCtrl
from src.Controllers.WebImageProcessingCtrl import WebImageProcessingCtrl as WebCtrl
from src.Controllers.AppProcessingCtrl import AppProcessingCtrl as AppCtrl

app = Flask(__name__)
port = 6000

@app.post('/imageProcessing')
def ProcessImage():
    platform = request.args.get("platform")
    print(platform)
    if platform == "Unity":
        print("Get request from Unity")
        unitCtrl = UnitCtrl()
        data2send = unitCtrl.MediaProcessing(request)
    elif platform == "GeosystemApp":
        print("Get request from GeosystemApp")
        webCtrl = WebCtrl()
        data2send = webCtrl.MediaProcessing(request)
    elif platform == "Application":
        print('Get request from Application')
        appCtrl = AppCtrl(True, "ImageApp")
        data2send = appCtrl.MediaProcessing(request)
    else: 
        data2send = {
            'status': 400,
            'message': "Неверные параметры запроса",
        }
    return jsonify(data2send)

@app.post('/videoProcessing')
def ProcessVideo():
    platform = request.args.get("platform")
    if platform == "Application":
        print('Get request from Application')
        appCtrl = AppCtrl(False, "VideoApp")
        data2send = appCtrl.MediaProcessing(request)
    else: 
        data2send = {
            'status': 400,
            'message': "Неверные параметры запроса",
        }
    return jsonify(data2send)

if __name__ == '__main__':
    app.run(debug=True, port=port)