import cv2
import src.Config.config as config
from ultralytics import YOLO
from torchvision.transforms import ToTensor
from src.Middlewares.IOUHandler import IOUHandler
from src.Middlewares.PlatformHandler import PlatformHandler

class ModelProcessing:
    def __init__(self, typeRequest):
        self.model = YOLO(config.model_path)
        self.__ioulimit = 0.3
        self.__typeRequestKey = typeRequest

    def DetectingObjects(self, file):
        image = PlatformHandler.ImageRequestTransform(self.__typeRequestKey, file)

        h, w, _ = image.shape
        print(w, h)
        resized_image = cv2.resize(image, (640, 640))
        tensor_image = ToTensor()(resized_image).unsqueeze(0)
        result = self.model(tensor_image)[0]

        boxes_data = result.boxes.data.cpu().numpy()
        boxes_data = IOUHandler.RemoveSmallBigBoxes(boxes_data, (w, h), 0.1)
        boxes_data = IOUHandler.RemoveInnerBoxes(boxes_data, self.__ioulimit)
        boxes_data[:, :4:2] = boxes_data[:, :4:2] / 640 * w
        boxes_data[:, 1:4:2] = boxes_data[:, 1:4:2] / 640 * h
        annotated_image = image.copy()
        for box in boxes_data:
            x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            annotated_image = cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (255,0,0), 2)

        return PlatformHandler.ImageResponseTransform(self.__typeRequestKey, annotated_image, boxes_data)

    