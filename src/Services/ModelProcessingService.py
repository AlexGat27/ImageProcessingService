import cv2 #Импорт для работы с изображениями
import src.Config.config as config #Импорт для получения пути модели
from ultralytics import YOLO #Испорт для инициализации модели 
from torchvision.transforms import ToTensor #Импорт для преобразования numpy изображения в тензор
from src.Middlewares.IOUHandler import IOUHandler #Импорт для удаления лишних bounding box
from src.Middlewares.PlatformHandler import PlatformHandler #Импорт для контроля запроса с разных платформ

class ModelProcessing:
    #Инициализация полей класса
    def __init__(self, typeRequest):
        self.model = YOLO(config.model_path) #Модель 
        self.__ioulimit = 0.3 #Минимальное допустимое пересечение bounding box
        self.__typeRequestKey = typeRequest #Ключ платформы

    #Обработка изображения моделью и получение bounding box 
    def DetectingObjects(self, file):
        image = PlatformHandler.ImageRequestTransform(self.__typeRequestKey, file) #Изображение в нужном формате
        h, w, _ = image.shape
        resized_image = cv2.resize(image, (640, 640)) #Изменение размеров изображения под модель нейросети
        tensor_image = ToTensor()(resized_image).unsqueeze(0) #Преобразование numpy в тензор
        result = self.model(tensor_image)[0] #Обработка тензора моделью

        boxes_data = result.boxes.data.cpu().numpy() #Получение информации о bounding box
        boxes_data = IOUHandler.RemoveSmallBigBoxes(boxes_data, (w, h), 0.01) #Удаление малых bounding box 
        boxes_data = IOUHandler.RemoveInnerBoxes(boxes_data, self.__ioulimit) #Удаление внутренних bounding box
        #Преобразование координат вершин bounding box под оригинальный размер изображения
        boxes_data[:, :4:2] = boxes_data[:, :4:2] / 640 * w
        boxes_data[:, 1:4:2] = boxes_data[:, 1:4:2] / 640 * h
        annotated_image = image.copy()
        #Отрисовка bounding box
        for box in boxes_data:
            x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            annotated_image = cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (255,0,0), 2)

        return PlatformHandler.ImageResponseTransform(self.__typeRequestKey, annotated_image, boxes_data) #Возвращение данных в нужном формате

    