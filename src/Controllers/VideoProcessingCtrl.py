from MediaProcessingInterface import *
from src.Services.DistTracker import DistTracker 
from src.Services.ModelProcessingService import ModelProcessing
from src.Middlewares.IOUHandler import IOUHandler

class VideoProcessingCtrl(MediaProcessingInterface):

    def __init__(self, iouLim):
        self.__iouLim = iouLim
        self.__tracker = DistTracker()
        self.__modelProcessingService = ModelProcessing()

    def MediaProcessing(self, request: Request):
        video_path = request.form["videoPath"]
        cap = cv2.VideoCapture(video_path)

        while cap.isOpened():
            success, frame = cap.read()
            if success:
                filter_frame = frame.copy()
                
                frame, boxes, _ = self.__modelProcessingService.DetectingObjects(frame, "Someone")
                # Фильтрация и трекинг
                boxes = IOUHandler.RemoveSmallBoxes(boxes, self.__iouLim)
                boxes_ids = self.__tracker.update(boxes)

                for box_id in boxes_ids:
                    x1, y1, x2, y2, id = box_id
                    cv2.rectangle(filter_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(filter_frame, (x1, y1), (x1+100, y1+50), (0, 0, 0), -1)
                    cv2.putText(filter_frame, "ID: "+str(id), (x1+10, y1+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
                filter_frame = cv2.resize(filter_frame, (filter_frame.shape[1]//2, filter_frame.shape[0]//2))
                cv2.imshow("All boxes", frame)
                cv2.imshow("Filter boxes", filter_frame)

                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()