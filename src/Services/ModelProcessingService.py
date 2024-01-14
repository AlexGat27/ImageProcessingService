import cv2
import numpy as np
import src.Config.config as config
from ultralytics import YOLO
from torchvision.transforms import ToTensor

class ModelProcessing:
    def __init__(self):
        self.model = YOLO(config.model_path)

    def modelProcessing(self, file):
        # image_np = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file, cv2.IMREAD_COLOR)

        h, w, _ = image.shape

        resized_image = cv2.resize(image, (640, 640))
        tensor_image = ToTensor()(resized_image).unsqueeze(0)
        result = self.model(tensor_image)[0]

        boxes_data = result.boxes.data.cpu().numpy()
        bboxes = boxes_data[:, :4]
        bboxes[:, ::2] = bboxes[:, ::2] / 640 * w
        bboxes[:, 1::2] = bboxes[:, 1::2] / 640 * h

        annotated_image = image.copy()
        for box in boxes_data:
            x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            print(x1, y1, x2, y2)
            annotated_image = cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (255,0,0), 2)

        bboxes[:, ::2] -= w/2
        bboxes[:, 1::2] -= h/2

        return annotated_image, bboxes, boxes_data[:, 4:]