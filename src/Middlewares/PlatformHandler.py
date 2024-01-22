import numpy as np
import cv2

class PlatformHandler:

    @staticmethod
    def ImageRequestTransform(requestKey: str, image: any):
        if requestKey == "VideoApp":
            return image
        else:
            return cv2.imdecode(image, cv2.IMREAD_COLOR)

    @staticmethod
    def ImageResponseTransform(requestKey: str, image: np.array, boxes_data: np.array):
        if requestKey == "Web":
            return cv2.imencode('.jpg', image)[1].tobytes(), boxes_data.shape[0]
        elif requestKey == "Unity":
            boxes_data[:, :4:2] -= image.shape[1]//2
            boxes_data[:, 1:4:2] -= image.shape[0]//2
        return image, boxes_data[:, :4]