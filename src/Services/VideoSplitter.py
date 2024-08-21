import os
import cv2
import numpy as np

from src.Config.boxesConf import aroundBoxesCoef
from src.Models.Camera import Camera

class VideoSplitter:
    def __init__(self, resultsFolder, cam: Camera, defaultInterval=None):
        self.__resultsFolder = resultsFolder
        if defaultInterval is None:
            print(cam)
            self.__interval = int(cam.fps * (2 * cam.height * np.tan(cam.fieldOfView * np.pi / 360) * (1 - aroundBoxesCoef * 2)) / cam.speed)
        else: self.__interval = defaultInterval
        print(f"Интервал: {self.__interval}")

    def SplitVideo(self, video_path: str):
        video_name = video_path.split('/')[-1].split('.')[0]
        saveFolder = os.getcwd() + f'/results/{self.__resultsFolder}/{video_name}'
        if os.path.exists(saveFolder):
            saveFolder += '_' + str(len(os.listdir(os.getcwd() + f'/results/{self.__resultsFolder}')))
        os.makedirs(saveFolder)
        cap = cv2.VideoCapture(video_path)
        frameCount = 0
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                if frameCount % self.__interval == 0:
                    filename = f'{saveFolder}/frame_{video_name}_{frameCount}.jpg'
                    cv2.imwrite(filename, frame)
                frameCount+=1
                cv2.imshow("Video", frame)
                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                    break
            else:
                print("система не прочиатала файл")
                break

        # Release the video capture object and close the display window
        cap.release()
        cv2.destroyAllWindows()
        return saveFolder