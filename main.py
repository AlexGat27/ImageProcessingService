from flask import Flask, request, jsonify, abort
from Controllers.UnityProcessingCtrl import UnityProcessingCtrl as UnitCtrl
from Controllers.WebImageProcessingCtrl import WebImageProcessingCtrl as WebCtrl

app = Flask(__name__)
port = 6000

@app.post('/imageProcessing')
def ProcessMedia():
    platform = request.args.get("platform")
    if platform == "Unity":
        print("Get request from Unity")
        unitCtrl = UnitCtrl()
        data2send = unitCtrl.MediaProcessing(request)
    elif platform == "GeosystemApp":
        print("Get request from App")
        webCtrl = WebCtrl()
        data2send = webCtrl.MediaProcessing(request)
    else: 
        data2send = {
            'status': 400,
            'message': "Неверные параметры запроса",
        }
    return jsonify(data2send)

if __name__ == '__main__':
    app.run(debug=True, port=port)