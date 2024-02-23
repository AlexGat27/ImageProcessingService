import os
import cv2
import numpy as np
import boto3

class ImageSaver:

    def __init__(self, saveFolder=os.curdir):
        self.saveFolder = saveFolder
        self.session = boto3.Session()
        self.s3 = self.session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )

    def SaveImage(self, image: np.array) -> str:
        if not(os.path.exists(self.saveFolder)):
            os.makedirs(self.saveFolder)
        countFiles = len(os.listdir(self.saveFolder))
        path = self.saveFolder + f'/process_image_{countFiles}.png'
        cv2.imwrite(path, image)
        self.s3.upload_file(path, 'pothole', f'/process_image_{countFiles}.png')
        return self.saveFolder + f'\process_image_{countFiles}.png'