from flask import Flask, request, jsonify, abort
from src.Controlllers.MediaProcessingCtrl import MediaProcessingCtrl
import base64
import numpy as np

app = Flask(__name__)
port = 5000

@app.post('/imageProcessing')
def process_media():
    mediaCtrl = MediaProcessingCtrl()
    data2send = mediaCtrl.UnityProcessMedia(request)
    return jsonify(data2send)

if __name__ == '__main__':
    app.run(debug=True, port=port)