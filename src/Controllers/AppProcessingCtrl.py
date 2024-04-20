import base64
from src.Models.Camera import Camera
from src.Controllers.MediaProcessingInterface import *
from src.Services.DistTracker import DistTracker 
from src.Services.ModelProcessingService import ModelProcessing
from src.Services.CRSConverterService import CRSConverter
from src.Services.ImageSaverService import ImageSaver
from src.Services.VideoSplitter import VideoSplitter
from src.Services.Pixels2MetresConverterService import Pixels2MetresConverter
import random

class AppProcessingCtrl(MediaProcessingInterface):

    def __init__(self, typeRequestKey: str):
        self.__modelProcessingService = ModelProcessing(typeRequestKey)

    def SplitVideo(self, req: Request, is_image: bool):
        camera = Camera(fieldOfView=float(req.form["fieldOfView"]), height=float(req.form["height"]),
                        fps=float(req.form["fps"]), speed=float(req.form["speed"]))
        if int(req.form["defaultInterval"]) > 10:
            self.__videoSplitter = VideoSplitter('SplitVideos', camera, int(req.form["defaultInterval"]))
        else: self.__videoSplitter = VideoSplitter('SplitVideos', camera)
        if not(is_image):
            return {'frames_path': self.__videoSplitter.SplitVideo(req.form["video_path"])}

    def MediaProcessing(self, req: Request, is_image = True) -> list:
        if is_image:
            camera = Camera(fieldOfView=float(req.form["fieldOfView"]), height=float(req.form["height"]),
                            coords=np.asarray([req.form["camX"], req.form["camY"]], float), 
                            angle=np.asarray([0,0,req.form["angleZ"]], float))
            file_content = base64.b64decode(req.form['image'].encode('utf-8'))
            return self.__imageProcessing(file_content, 
                                          camera,
                                          req.form["nameTable"])

    def __imageProcessing(self, image_bytes, camera: Camera, nameTable = None) -> list:
        data2send = []
        image_array = np.asarray(bytearray(image_bytes), dtype=np.uint8)  # Преобразуем изображение в массив байтов
        frame, boxes = self.__modelProcessingService.DetectingObjects(image_array) 
        camera.resolution = frame.shape[:2]
        frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
        image_path = ImageSaver.SaveImage(frame, nameTable)
        for box in boxes:
            coord3857 = Pixels2MetresConverter.ConvertProcessing(box, camera) + camera.coords
            coord4326 = CRSConverter.Epsg3857To4326(coord3857)
            data2send.append({
                        'crs3857': {'x': coord3857[0], 'y': coord3857[1]},
                        'crs4326': {'lon': coord4326[0], 'lat': coord4326[1]},
                        'image_path': image_path
                    })
        return data2send