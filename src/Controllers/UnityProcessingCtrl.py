from src.Controllers.MediaProcessingInterface import *
from src.Services.ImageSaverService import ImageSaver
from src.Services.ModelProcessingService import ModelProcessing
from src.Services.CRSConverterService import CRSConverter
from src.Services.Pixels2MetresConverterService import Pixels2MetresConverter

class UnityProcessingCtrl(MediaProcessingInterface):

    def __init__(self):
        self._data2send = np.array([{'crs3857': {'x': 0, 'y': 0},
                                    'crs4326': {'x': 0, 'y': 0}}])
        self._modelService = ModelProcessing()
        self._imageSaver = ImageSaver("Assets/Processed_images")

    def MediaProcessing(self, req: Request):
        file = req.files["image"].read()
        cameraFieldOfView = self.__convertReqType(req.form["fieldOfView"], float)
        cameraHeight = self.__convertReqType(req.form["cameraHeight"], float)
        cameraAzimut = self.__convertReqType(req.form["cameraAzimut"], float)
        cameraPosition3857 = self.__convertReqType([req.form["cameraX"], req.form["cameraY"]], float)
        screenResolution = self.__convertReqType([req.form["screenWidth"], req.form["screenHeight"]], int)

        new_image_np = np.frombuffer(file, np.uint8)

        result_image, potholesData, _ = self._modelService.DetectingObjects(new_image_np, "Unity")
        self._imageSaver.SaveImage(result_image)
        potholes_coordinates_3857 = Pixels2MetresConverter.ConvertProcessing(potholesData, camFieldOfView=cameraFieldOfView, 
        camAzimut=cameraAzimut, camHeight=cameraHeight, camResolution=screenResolution) + cameraPosition3857
        potholes_coordinates_4326 = CRSConverter.Epsg3857To4326(potholes_coordinates_3857)
        for coord3857, coord4326 in zip(potholes_coordinates_3857, potholes_coordinates_4326):
            self._data2send = np.append(self._data2send, {'crs3857': {'x': coord3857[0], 'y': coord3857[1]},
                                        'crs4326': {'x': coord4326[0], 'y': coord4326[1]}})
        return self._data2send[1:].tolist()
    
    def __convertReqType(self, req, _type: type):
        if type(req) == str:
            splitStr = req.split(',')
            if len(splitStr) > 1:
                return (_type(splitStr[0]) + _type(splitStr[1])/pow(10, len(splitStr[1])))
            else:
                return _type(req)
        else:
            splitStr1 = req[0].split(',')
            splitStr2 = req[1].split(',')
            if len(splitStr1) > 1 or len(splitStr2) > 1:
                return np.array([_type(splitStr1[0]) + _type(splitStr1[1])/pow(10, len(splitStr1[1])),
                                 _type(splitStr2[0]) + _type(splitStr2[1])/pow(10, len(splitStr2[1]))])
            else: return np.asarray(req, _type)
    

