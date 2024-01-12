import os
import cv2
import numpy as np

class ImageSaverService:

    def __init__(self, saveFolder=os.curdir):
        self.saveFolder = saveFolder

    def saveImage(self, image: np.array):
        if not(os.path.exists(self.saveFolder)):
            os.makedirs(self.saveFolder)
        countFiles = len(os.listdir(self.saveFolder))
        print(self.saveFolder + f'/process_image{countFiles}')
        cv2.imwrite(self.saveFolder + f'/process_image_{countFiles}.png', image)
        print("Succesfuly saving processed image")