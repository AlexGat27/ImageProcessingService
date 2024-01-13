import cv2
import numpy as np
import src.Config.config as config
from ultralytics import YOLO
from torchvision.transforms import ToTensor
from src.Services.ImageSaverService import ImageSaverService

class ModelProcessing:
    def __init__(self):
        self.model = YOLO(config.model_path)

    def modelProcessing(self, file):
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
        boxes_data[:, ::2] = boxes_data[:, ::2] / 640 * w - w/2
        boxes_data[:, 1::2] = boxes_data[:, 1::2] / 640 * h - h/2
        return result.plot(), boxes_data