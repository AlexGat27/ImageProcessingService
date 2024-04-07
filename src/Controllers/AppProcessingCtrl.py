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
            return self.__imageProcessing(req.files['image'], 
                                          camera,
                                          req.form["nameTable"])
        # else:
        #     return self.__videoProcessing(req.form['video_path'], 
        #                                   req.form["nameTable"]) 

    # def __videoProcessing(self, video_path, is_save, nameTable = None) -> list:
    #     data2send = []
    #     tracker = DistTracker()
    #     if is_save: imageSaver = ImageSaver(f'{ImagesSavedPath}/{nameTable}')

    #     cap = cv2.VideoCapture(video_path)
    #     countFrame = 0
    #     count_ids = -1
    #     while cap.isOpened():
    #         success, frame = cap.read()
    #         if success:
    #             if countFrame % 5 == 0:
    #                 frame, boxes = self.__modelProcessingService.DetectingObjects(frame)
    #                 boxes_ids = np.asarray(tracker.update(boxes), int)
    #                 print(boxes_ids)

    #                 for box_id in boxes_ids:
    #                     x1, y1, x2, y2, id = box_id
    #                     frame = cv2.rectangle(frame, (x1, y1), (x1+100, y1+50), (0, 0, 0), -1)
    #                     frame = cv2.putText(frame, "ID: "+str(id), (x1+10, y1+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    #                     if id > count_ids:
    #                         x, y = random.uniform(3360000, 3400000), random.uniform(8370000, 8400000)
    #                         lon, lat = CRSConverter.Epsg3857To4326(np.array([x, y]))
    #                         data2send.append({
    #                             'crs3857': {'x': x, 'y': y},
    #                             'crs4326': {'lon': lon, 'lat': lat}
    #                         })
    #                         imageSaver.SaveImage(frame)
    #                         count_ids = id
    #             countFrame+=1
    #             cv2.imshow("wewecw", cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2)))
    #             k = cv2.waitKey(1) & 0xFF
    #             if k == 27:
    #                 break
    #         else:
    #             break
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     return data2send

    def __imageProcessing(self, image_file, camera: Camera, nameTable = None) -> list:
        data2send = []
        image_array = np.asarray(bytearray(image_file.read()), dtype=np.uint8)  # Преобразуем изображение в массив байтов
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