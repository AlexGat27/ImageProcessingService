from flask import Flask, request, jsonify, abort
from Controllers.UnityProcessingCtrl import UnityProcessingCtrl as UnitCtrl
from Controllers.WebImageProcessingCtrl import WebImageProcessingCtrl as WebCtrl

app = Flask(__name__)
port = 5000

@app.post('/imageProcessing/unity')
def UnityProcessMedia():
    unitCtrl = UnitCtrl()
    data2send = unitCtrl.MediaProcessing(request)
    return jsonify(data2send)

@app.post('/imageProcessing/GeosystemApp')
def UnityProcessMedia():
    webCtrl = WebCtrl()
    data2send = webCtrl.MediaProcessing(request)
    return jsonify(data2send)

if __name__ == '__main__':
    app.run(debug=True, port=port)