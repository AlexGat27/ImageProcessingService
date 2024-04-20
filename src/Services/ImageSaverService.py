import os #Работа с файловой системой
import cv2 #В данном сервисе используется для сохранения фото
import numpy as np #Математические операции
from datetime import datetime #Импорт для именования файлов фотографий исходя из времени

#Класс сохранения фотографий
class ImageSaver:

    @staticmethod
    def SaveImage(image: np.array, nameFolder: str) -> str: #Статический метод сохранения фото
        saveFolder = os.getcwd() + f'/results/{nameFolder}'
        print(saveFolder)
        if (not(os.path.exists(saveFolder))):
            os.mkdir(saveFolder)
        countFiles = len(os.listdir(saveFolder))
        image_name = f'image_{datetime.now().strftime("%Y-%m-%d")}_{countFiles}.png'
        cv2.imwrite(f'{saveFolder}/{image_name}', image)
        if (os.environ.get('save_path')):
            print(f'{os.environ.get("save_path")}/{nameFolder}/{image_name}')
            return f'{os.environ.get("save_path")}/{nameFolder}/{image_name}'
        else:
            print(f'{saveFolder}/{image_name}')
            return f'{saveFolder}/{image_name}'