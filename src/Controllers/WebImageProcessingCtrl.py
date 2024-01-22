import base64
import random
import src.Config.config as config
from src.Controllers.MediaProcessingInterface import *
from src.Services.ModelProcessingService import ModelProcessing
from src.Middlewares.CheckSimilarImages import CheckSimilarImages

class WebImageProcessingCtrl():

    def __init__(self):
        self.data2send = {
            'status': 0,
            'message': None,
            'potholesData': None,
            'imageUrl': None
        }
        self.checkService = CheckSimilarImages()
        self.modelProcessing = ModelProcessing("Web")

    def MediaProcessing(self, req: Request):
        if 'image' not in req.files:
            self.data2send['status'] = 400
            self.data2send['message'] = "Неккоректный запрос. Изображения нет в параметрах запроса"
            return self.data2send
        
        file = req.files['image']
        new_image_np = np.frombuffer(file.read(), np.uint8)
        old_image_paths = req.form.getlist('old_image_paths')  
        checkSimilarityResult = self.checkService.CheckSimilarity(new_image_np, old_image_paths)
        if checkSimilarityResult:
            self.data2send['status'] = 452
            self.data2send['message'] = 'Ошибка, такое изображение уже есть в базе данных'
            return self.data2send

        output_buffer, countPotholes = self.modelProcessing.DetectingObjects(new_image_np, "Web")
        if countPotholes < 1:
            self.data2send['status'] = 404
            self.data2send['message'] = 'Ошибка, ям не найдено'
            return self.data2send
        res_send = base64.b64encode(output_buffer).decode('utf-8')

        potholesData = []
        for i in range(countPotholes):
            potholesData.append({
                "nametable": "pothole",
                "street": random.choice(config.street),
                "lat": random.uniform(3360000, 3400000),
                "lon": random.uniform(8370000, 8400000),
                "class": random.randint(1,4)
            })

        self.data2send['status'] = 200
        self.data2send['imageUrl'] = res_send
        self.data2send['potholesData'] = potholesData
        return self.data2send