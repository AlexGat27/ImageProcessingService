import numpy as np
class Camera:
    def __init__(self, fieldOfView: float = 0,
                height = 0,
                coords: np.array = np.array([0,0,0]), 
                angle: np.array = np.array([0,0,0]), 
                resolution: np.array = np.array([0,0])):
        self.height = height    
        self.fieldOfView = fieldOfView
        self.coords = coords
        self.angle = angle
        self.resolution = resolution