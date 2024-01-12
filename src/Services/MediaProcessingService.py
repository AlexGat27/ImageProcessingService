import cv2
import numpy as np
import src.Config.config as config
from ultralytics import YOLO
from torchvision.transforms import ToTensor
from src.Services.ImageSaverService import ImageSaverService

class MediaProcessingService:
    def __init__(self):
        self.model = YOLO(config.model_path)
        self.imageSaver = ImageSaverService("Assets/Processed_images")

    def imageProcessing(self, file):
        potholesData = []

        # image_np = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file, cv2.IMREAD_COLOR)

        h, w, _ = image.shape

        image = cv2.resize(image, (640, 640))
        tensor_image = ToTensor()(image).unsqueeze(0)
        result = self.model(tensor_image)[0]

        image2save = cv2.resize(result.plot(), (w, h))
        self.imageSaver.saveImage(image2save)

        boxes_data = result.boxes.data.cpu().numpy()
        boxes = np.asarray([box[:4] for box in boxes_data], dtype=float)
        boxes[:, ::2], boxes[:, 1::2] = boxes[:, ::2] / 640 * w - w/2, boxes[:, 1::2] / 640 * h - h/2
        # print(boxes_data)
        # print(boxes)

        for box in boxes:
            potholesData.append({
                'x': str((box[0] + box[2]) // 2),
                'y': str((box[1] + box[3]) // 2)
            })
        print(potholesData)
        return potholesData