from abc import ABC, abstractmethod
from flask import Request
import numpy as np
import cv2

class MediaProcessingInterface(ABC):

    @abstractmethod
    def __init__(self, *args) -> None:
        pass

    @abstractmethod
    def MediaProcessing(self, request: Request):
        pass