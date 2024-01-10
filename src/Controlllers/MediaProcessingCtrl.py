import base64
import numpy as np
from src.Services.MediaProcessingService import MediaProcessingService
from src.Services.CheckSimilarImagesService import CheckSimilarImagesService
from flask import Request
from time import time

class MediaProcessingCtrl:

    def __init__(self):
        self.data2send = {
            'status': 0,
            'message': None,
            'potholesData': None,
            'imageUrl': None
        }
        self.checkService = CheckSimilarImagesService()
        self.mediaService = MediaProcessingService()

    def process_media(self, req: Request):
        if 'image' not in req.files:
            self.data2send['status'] = 400
            self.data2send['message'] = "Неккоректный запрос. Изображения нет в параметрах запроса"
            return self.data2send
        
        file = req.files['image']
        new_image_np = np.frombuffer(file.read(), np.uint8)
        old_image_paths = req.form.getlist('old_image_paths')  
        checkSimilarityResult = self.checkService.checkSimilarity(new_image_np, old_image_paths)
        if checkSimilarityResult:
            self.data2send['status'] = 452
            self.data2send['message'] = 'Ошибка, такое изображение уже есть в базе данных'
            return self.data2send

        t = time()
        output_buffer, potholesData = self.mediaService.imageProcessing(new_image_np)
        print(time()-t)
        if not(potholesData):
            self.data2send['status'] = 404
            self.data2send['message'] = 'Ошибка, ям не найдено'
            return self.data2send
        res_send = base64.b64encode(output_buffer).decode('utf-8')
        
        self.data2send['status'] = 200
        self.data2send['imageUrl'] = res_send
        self.data2send['potholesData'] = potholesData
        return self.data2send
