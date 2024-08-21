from src.Models.Camera import Camera #Импорт модели камеры
from src.Controllers.MediaProcessingInterface import * #Импорт интерфейса контроллеров
from src.Services.ImageSaverService import ImageSaver #Импорт сервиса сохранения изображений
from src.Services.ModelProcessingService import ModelProcessing #Импорт сервиса обработки изображений моделью 
from src.Services.CRSConverterService import CRSConverter #Импорт сервиса преобразования СКС
from src.Services.Pixels2MetresConverterService import Pixels2MetresConverter #Импорт сервиса преобразования пикселей в метры

class UnityProcessingCtrl(MediaProcessingInterface): #Контроллер запросов, подаваемых с платформы Unity

    def __init__(self):
        self._data2send = np.array([{'crs3857': {'x': 0, 'y': 0},
                                    'crs4326': {'x': 0, 'y': 0}}]) #Данные, передаваемые обратно на платформу Unity
        self._camera = Camera() #Объект камеры
        self._modelService = ModelProcessing("Unity") #Объект сервиса обработки изображений моделью

    #Метод обработки данных с Unity
    def MediaProcessing(self, req: Request):
        #Получение всех данных из запроса
        file = req.files["image"].read()
        self._camera.fieldOfView = self.__convertReqType(req.form["fieldOfView"], float)
        self._camera.height = self.__convertReqType(req.form["cameraHeight"], float)
        self._camera.angle[2] = self.__convertReqType(req.form["cameraAzimut"], float)
        self._camera.coords = self.__convertReqType([req.form["cameraX"], req.form["cameraY"]], float)
        self._camera.resolution = self.__convertReqType([req.form["screenWidth"], req.form["screenHeight"]], int)

        new_image_np = np.frombuffer(file, np.uint8) #Получение numpy из буфера

        result_image, potholesData = self._modelService.DetectingObjects(new_image_np) #Обработка изображения и получение данных о ямах
        ImageSaver.SaveImage(result_image, "UnityImages") #Сохранение изображений
        for pothole in potholesData: #Конвертация координат каждой обнаруженной ямы
            coord3857 = Pixels2MetresConverter.ConvertProcessing(pothole, self._camera) + self._camera.coords
            coord4326 = CRSConverter.Epsg3857To4326(coord3857)
            self._data2send = np.append(self._data2send, {'crs3857': {'x': coord3857[0], 'y': coord3857[1]},
                                    'crs4326': {'x': coord4326[0], 'y': coord4326[1]}})
        return self._data2send[1:].tolist()
    
    #Конвертация строк запроса в нужные форматы данных
    def __convertReqType(self, req, _type: type):
        if type(req) == str:
            splitStr = req.split(',')
            if len(splitStr) > 1:
                return (_type(splitStr[0]) + _type(splitStr[1])/pow(10, len(splitStr[1])))
            else:
                return _type(req)
        else:
            print(req)
            splitStr1 = req[0].split(',')
            splitStr2 = req[1].split(',')
            value1 = _type(splitStr1[0]) + _type(splitStr1[1])/pow(10, len(splitStr1[1])) if len(splitStr1) > 1 else _type(splitStr1[0])
            value2 = _type(splitStr2[0]) + _type(splitStr2[1])/pow(10, len(splitStr2[1])) if len(splitStr2) > 1 else _type(splitStr2[0])
            return np.array([value1,value2])
