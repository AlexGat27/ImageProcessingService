from flask import Flask, request, jsonify, make_response
from src.Controllers.AppProcessingCtrl import AppProcessingCtrl as AppCtrl

tkinterApp = Flask("TkinterApp")

@tkinterApp.post('/imageProcessing')
def ImageProcessingTkinter():
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

@tkinterApp.post('/videoSplit')
def SplitVideo():
    print('Get request from Application')
    appCtrl = AppCtrl("VideoApp")
    data2send = appCtrl.SplitVideo(request, False)
    return jsonify(data2send)

if __name__ == '__main__':
    tkinterApp.run(debug=True, port=6002)