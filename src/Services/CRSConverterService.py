import numpy as np

class CRSConverter:

    __HALF_EQUATOR = 20037508.34

    @staticmethod
    def Epsg3857To4326(crs3857: np.array):
        crs4356 = crs3857.copy()
        crs4356[:, 0] = (crs3857[:, 0] / CRSConverter.__HALF_EQUATOR) * 180
        crs4356[:, 1] = np.arctan(np.exp(((crs3857[:, 1] / CRSConverter.__HALF_EQUATOR) * 180) * np.pi / 180)) / (np.pi / 360) - 90
        return crs4356
