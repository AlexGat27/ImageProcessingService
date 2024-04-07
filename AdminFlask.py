from flask import Flask, request, jsonify, make_response
from src.Controllers.AppProcessingCtrl import AppProcessingCtrl as AppCtrl

adminApp = Flask("AdminApp")

@adminApp.post('/imageProcessing')
def ImageProcessingAdmin():
    print('Get request from Application')
    appCtrl = AppCtrl("ImageApp")
    data2send = appCtrl.MediaProcessing(request, True)
    return jsonify(data2send)
    
# @tkinterApp.post('/videoProcessing')
# def ProcessVideo():
#     print('Get request from Application')
#     appCtrl = AppCtrl("VideoApp")
#     data2send = appCtrl.MediaProcessing(request, False)
#     return jsonify(data2send)

@adminApp.post('/videoSplit')
def SplitVideo():
    print('Get request from Application')
    appCtrl = AppCtrl("VideoApp")
    data2send = appCtrl.SplitVideo(request, False)
    return jsonify(data2send)

if __name__ == '__main__':
    adminApp.run(debug=True, port=6002)