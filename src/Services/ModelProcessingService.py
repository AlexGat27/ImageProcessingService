import cv2 #Импорт для работы с изображениями
import src.Config.config as config #Импорт для получения пути модели
import src.Config.boxesConf as boxconfig
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
        self.__iouHandler = IOUHandler()
        self.__platformHandler = PlatformHandler()

    #Обработка изображения моделью и получение bounding box 
    def DetectingObjects(self, file):
        image = self.__platformHandler.ImageRequestTransform(self.__typeRequestKey, file) #Изображение в нужном формате
        h, w, _ = image.shape
        resized_image = cv2.resize(image, (640, 640)) #Изменение размеров изображения под модель нейросети
        tensor_image = ToTensor()(resized_image).unsqueeze(0) #Преобразование numpy в тензор
        result = self.model(tensor_image)[0] #Обработка тензора моделью

        boxes_data = result.boxes.data.cpu().numpy() #Получение информации о bounding box
        boxes_data = self.__iouHandler.RemoveSmallBigBoxes(boxes_data, (640, 640), boxconfig.smallBigBoxesCoef) #Удаление малых bounding box 
        boxes_data = self.__iouHandler.RemoveInnerBoxes(boxes_data, self.__ioulimit) #Удаление внутренних bounding box
        boxes_data = self.__iouHandler.RemoveAroundBoxes(boxes_data, (640, 640), boxconfig.aroundBoxesCoef)
        #Преобразование координат вершин bounding box под оригинальный размер изображения
        print(boxes_data)
        boxes_data[:, :4:2] = boxes_data[:, :4:2] / 640 * w
        boxes_data[:, 1:4:2] = boxes_data[:, 1:4:2] / 640 * h
        annotated_image = image.copy()
        #Отрисовка bounding box
        for box in boxes_data:
            x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            annotated_image = cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (255,0,0), 2)

        return self.__platformHandler.ImageResponseTransform(self.__typeRequestKey, annotated_image, boxes_data) #Возвращение данных в нужном формате

    