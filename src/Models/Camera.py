import numpy as np #Импорт для создания numpy массивов
#Моедль камеры с необхожимыми параметрами
class Camera:
    #Инициализация необходимых параметров камеры
    def __init__(self, fieldOfView: float = 0, #Угол обзора
                height = 0, #Высота 
                coords: np.array = np.array([0,0,0]), #Координаты камеры
                angle: np.array = np.array([0,0,0]), #Угол поворота по трем осям
                resolution: np.array = np.array([0,0]), #Разрешение камеры
                fps: float = 30, speed: float = 0): 
        self.height = height
        self.fieldOfView = fieldOfView
        self.coords = coords
        self.angle = angle
        self.resolution = resolution
        self.fps = fps
        self.speed = speed