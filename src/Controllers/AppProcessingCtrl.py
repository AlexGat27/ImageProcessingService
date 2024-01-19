from src.Controllers.MediaProcessingInterface import *
from src.Middlewares.IOUHandler import IOUHandler
from src.Config.config import ImagesSavedPath
from src.Services.DistTracker import DistTracker 
from src.Services.ModelProcessingService import ModelProcessing
from src.Services.CRSConverterService import CRSConverter
from src.Services.ImageSaverService import ImageSaver
import random

class AppProcessingCtrl(MediaProcessingInterface):

    def __init__(self, is_image, typeRequestKey: str):
        self.__modelProcessingService = ModelProcessing(typeRequestKey)
        self.__is_image = is_image

    def MediaProcessing(self, request: Request):
        if self.__is_image:
            image = request.files['image']
            return self.__imageProcessing(image, request.form["is_save_frame"], request.form["nameTable"])
        else:
            video_path = request.form['video_path']
            return self.__videoProcessing(video_path, request.form["is_save_frame"], request.form["nameTable"]) 

    def __videoProcessing(self, video_path, is_save, nameTable = None):
        data2send = []
        tracker = DistTracker()
        if is_save: imageSaver = ImageSaver(f'{ImagesSavedPath}/{nameTable}')

        cap = cv2.VideoCapture(video_path)
        countFrame = 0
        count_ids = -1
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                if countFrame % 5 == 0:
                    frame, boxes = self.__modelProcessingService.DetectingObjects(frame)
                    boxes_ids = np.asarray(tracker.update(boxes), int)
                    print(boxes_ids)

                    for box_id in boxes_ids:
                        x1, y1, x2, y2, id = box_id
                        frame = cv2.rectangle(frame, (x1, y1), (x1+100, y1+50), (0, 0, 0), -1)
                        frame = cv2.putText(frame, "ID: "+str(id), (x1+10, y1+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        if id > count_ids:
                            x, y = random.uniform(3360000, 3400000), random.uniform(8370000, 8400000)
                            lon, lat = CRSConverter.Epsg3857To4326(np.array([x, y]))
                            data2send.append({
                                'crs3857': {'x': x, 'y': y},
                                'crs4326': {'lon': lon, 'lat': lat}
                            })
                            imageSaver.SaveImage(frame)
                            count_ids = id
                countFrame+=1
                cv2.imshow("wewecw", cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2)))
                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
        return data2send

    def __imageProcessing(self, image_file, is_save, nameTable = None):
        data2send = []
        image_array = np.asarray(bytearray(image_file.read()), dtype=np.uint8)  # Преобразуем изображение в массив байтов
        
        frame, boxes = self.__modelProcessingService.DetectingObjects(image_array) 

        for box in boxes:
            x, y = random.uniform(3360000, 3400000), random.uniform(8370000, 8400000)
            lon, lat = CRSConverter.Epsg3857To4326(np.array([x, y]))
            data2send.append({
                        'crs3857': {'x': x, 'y': y},
                        'crs4326': {'lon': lon, 'lat': lat}
                    })
        if is_save:
            imageSaver = ImageSaver(f'{ImagesSavedPath}/{nameTable}')
            frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
            imageSaver.SaveImage(frame)
        return data2send