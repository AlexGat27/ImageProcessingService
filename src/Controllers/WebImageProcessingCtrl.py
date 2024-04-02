import base64
import src.Config.config as config
from src.Controllers.MediaProcessingInterface import *
from src.Services.ModelProcessingService import ModelProcessing
from src.Middlewares.CheckSimilarImages import CheckSimilarImages

class WebImageProcessingCtrl():

    def __init__(self):
        self.response = {
            'status': 0,
            'message': None,
            'countPotholes': 0,
            'imageUrl': None
        }
        self.checkService = CheckSimilarImages()
        self.modelProcessing = ModelProcessing("Web")

    def MediaProcessing(self, req: Request):
        print(req.form.get('old_image_paths'))
        if 'image' not in req.files:
            self.response['status'] = 453
            self.response['message'] = "Неккоректный запрос. Изображения нет в параметрах запроса"
            return self.response
        
        file = req.files['image']
        new_image_np = np.frombuffer(file.read(), np.uint8)
        old_image_paths = req.form.get('old_image_paths') 
        if old_image_paths:
            old_image_paths = old_image_paths.split('::')
            checkSimilarityResult = self.checkService.CheckSimilarity(new_image_np, old_image_paths)
            if checkSimilarityResult:
                self.response['status'] = 452
                self.response['message'] = 'Ошибка, такое изображение уже есть в базе данных'
                return self.response

        output_buffer, countPotholes = self.modelProcessing.DetectingObjects(new_image_np)
        if countPotholes < 1:
            self.response['status'] = 454
            self.response['message'] = 'Ошибка, ям не найдено'
            return self.response
        res_send = base64.b64encode(output_buffer).decode('utf-8')
        self.response['countPotholes'] = countPotholes
        self.response['status'] = 200
        self.response['imageUrl'] = res_send
        return self.response