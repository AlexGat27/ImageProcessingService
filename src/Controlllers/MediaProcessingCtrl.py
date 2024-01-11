import base64
import numpy as np
from src.Services.MediaProcessingService import MediaProcessingService
from flask import Request

class MediaProcessingCtrl:

    def __init__(self):
        self.data2send = {}
        self.mediaService = MediaProcessingService()

    def process_media(self, req: Request):
        # print(req.files)
        file = req.data
        new_image_np = np.frombuffer(file, np.uint8)

        potholesData = self.mediaService.imageProcessing(new_image_np)
        
        self.data2send = potholesData
        return self.data2send
