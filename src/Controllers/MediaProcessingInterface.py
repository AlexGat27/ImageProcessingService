from abc import ABC, abstractmethod
from flask import Request
import numpy as np
import cv2

#Интерфейс контроллеров
class MediaProcessingInterface(ABC):

    #Абстрактный метод инициализации полей
    @abstractmethod
    def __init__(self, *args) -> None:
        pass

    #Абстрактный метод обработки запроса
    @abstractmethod
    def MediaProcessing(self, request: Request):
        pass