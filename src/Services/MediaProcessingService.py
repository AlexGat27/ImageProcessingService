import cv2
import random
import numpy as np
import src.Config.config as config
from ultralytics import YOLO
from torchvision.transforms import ToTensor, Compose

class MediaProcessingService:
    def __init__(self):
        self.model = YOLO(config.model_path)

    def imageProcessing(self, file):
        potholesData = []

        # image_np = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file, cv2.IMREAD_COLOR)

        h, w, _ = image.shape

        image = cv2.resize(image, (640, 640))
        tensor_image = ToTensor()(image).unsqueeze(0)
        result = self.model(tensor_image)[0]
        for i in range(len(result.boxes)):
            potholesData.append({
                "nametable": "pothole",
                "street": random.choice(config.street),
                "lat": random.uniform(3360000, 3400000),
                "lon": random.uniform(8370000, 8400000),
                "class": random.randint(1,4)
            })
            # database.insert_to_table(nametable, time_detect, random.choice(__street),
            #                           random.uniform(3360000, 3400000), random.uniform(8370000, 8400000), random.randint(1,4))
        annotated_frame = result.plot()
        annotated_frame = cv2.resize(annotated_frame, (w, h))

        retval, buffer = cv2.imencode('.jpg', annotated_frame)
        output_buffer = buffer.tobytes()

        return output_buffer, potholesData