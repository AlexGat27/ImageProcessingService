import base64
import numpy as np
from Services.ImageSaverService import ImageSaverService
from Services.ModelProcessingService import ModelProcessing
from Services.CRSConverterService import CRSConverter
from Services.Pixels2MetresConverterService import Pixels2MetresConverter
from flask import Request

class MediaProcessingCtrl:

    def __init__(self):
        self._data2send = {}
        self._mediaService = ModelProcessing()
        self._imageSaver = ImageSaverService("Assets/Processed_images")

    def process_media(self, req: Request):
        file = req.files["image"]
        cameraFieldOfView = req.form["fieldOfView"]
        cameraHeight = req.form["cameraHeight"]
        cameraAzimut = req.form["cameraAzimut"]
        cameraPosition3857 = np.asrray([req.form["cameraX"], req.form["cameraY"]], float)
        screenResolution = np.asrray([req.form["screenWidth"], req.form["screenHeight"]], int)

        new_image_np = np.frombuffer(file, np.uint8)

        result_image, potholesData = self._mediaService.modelProcessing(new_image_np)
        self._imageSaver.saveImage(result_image)
        potholes_coordinates_3857 = Pixels2MetresConverter.ConvertProcessing(potholesData, camFieldOfView=cameraFieldOfView, 
        camAzimut=cameraAzimut, camHeight=cameraHeight, camResolution=screenResolution) + cameraPosition3857
        potholes_coordinates_4326 = CRSConverter.Epsg3857To4326(potholes_coordinates_3857)
        
        self.data2send = 
        return self.data2send
