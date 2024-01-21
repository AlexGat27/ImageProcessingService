import os
import cv2
from src.Services.ImageSaverService import ImageSaver

class VideoSplitter:
    def __init__(self, resultsFolder, interval):
        self.__resultsFolder = resultsFolder
        self.__interval = interval

    def SplitVideo(self, video_path: str):
        video_name = video_path.split('/')[-1].split('.')[0]
        saveFolder = self.__resultsFolder + video_name
        if os.path.exists(saveFolder):
            saveFolder += '_' + str(len(os.listdir(self.__resultsFolder)))
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