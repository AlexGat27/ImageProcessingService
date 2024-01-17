from src.Controllers.MediaProcessingInterface import *
from src.Middlewares.IOUHandler import IOUHandler
from src.Config.config import ImagesSavedPath
from src.Services.DistTracker import DistTracker 
from src.Services.ModelProcessingService import ModelProcessing
from src.Services.CRSConverterService import CRSConverter
from src.Services.ImageSaverService import ImageSaver
import random

class VideoProcessingCtrl(MediaProcessingInterface):

    def __init__(self, iouLim, folderName):
        self._iouLim = iouLim
        self._data2send = []
        self._tracker = DistTracker()
        self._modelProcessingService = ModelProcessing()
        self._imageSaver = ImageSaver(ImagesSavedPath + folderName)

    def MediaProcessing(self, request: Request):
        video_path = request.form["videoPath"]
        cap = cv2.VideoCapture(video_path)

        while cap.isOpened():
            success, frame = cap.read()
            count_ids = 0
            if success:
                filter_frame = frame.copy()
                
                frame, boxes, _ = self._modelProcessingService.DetectingObjects(frame, "Someone")
                if boxes.shape[0] <= 1:
                    continue
                # Фильтрация и трекинг
                boxes = IOUHandler.RemoveSmallBoxes(boxes, self._iouLim)
                boxes_ids = self._tracker.update(boxes)

                for box_id in boxes_ids:
                    x1, y1, x2, y2, id = box_id
                    cv2.rectangle(filter_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(filter_frame, (x1, y1), (x1+100, y1+50), (0, 0, 0), -1)
                    cv2.putText(filter_frame, "ID: "+str(id), (x1+10, y1+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                if len(boxes_ids) > count_ids and boxes.shape[0] > 0:
                    # frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
                    x, y = random.uniform(3360000, 3400000), random.uniform(8370000, 8400000)
                    lon, lat = CRSConverter.Epsg3857To4326(np.array([x, y]))
                    self._data2send.append({
                        'crs3857': {'x': x, 'y': y},
                        'crs4326': {'lon': CRSConverter.Epsg3857To4326(x), 'lat': CRSConverter.Epsg3857To4326(x)}
                    })
                    filter_frame = cv2.resize(filter_frame, (filter_frame.shape[1]//2, filter_frame.shape[0]//2))
                    self._imageSaver.SaveImage(filter_frame)
                    count_ids += len(boxes_ids) - count_ids
                # cv2.imshow("All boxes", frame)
                # cv2.imshow("Filter boxes", filter_frame)

                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                    break
            else:
                break
        return self._data2send
        cap.release()
        # cv2.destroyAllWindows()