import numpy as np
import cv2 #Импорт для декодирования изображений

#Класс посредник, преобразующий запросы в нужный формат 
class PlatformHandler:

    def ImageRequestTransform(self, requestKey: str, image: any): #Метод преобразования request
        if requestKey == "VideoApp":
            return image
        else:
            return cv2.imdecode(image, cv2.IMREAD_COLOR)

    def ImageResponseTransform(self, requestKey: str, image: np.array, boxes_data: np.array): #Метод преобразования response
        if requestKey == "Web":
            return cv2.imencode('.jpg', image)[1].tobytes(), boxes_data.shape[0]
        elif requestKey == "Unity": #Если платформа Unity, то продолжить перобразование 
            boxes_data[:, :4:2] -= image.shape[1]//2
            boxes_data[:, 1:4:2] -= image.shape[0]//2
        return image, boxes_data[:, :4]