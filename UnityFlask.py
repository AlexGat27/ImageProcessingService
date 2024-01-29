from flask import Flask, request, jsonify, make_response
from src.Controllers.UnityProcessingCtrl import UnityProcessingCtrl as UnitCtrl

unityApp = Flask("UnityApp")

@unityApp.post('/imageProcessing')
def ImageProcessingUnity():
    print("Get request from Unity")
    unitCtrl = UnitCtrl()
    data2send = unitCtrl.MediaProcessing(request)
    return jsonify(data2send)

if __name__ == '__main__':
    unityApp(debug=True, port=6002)