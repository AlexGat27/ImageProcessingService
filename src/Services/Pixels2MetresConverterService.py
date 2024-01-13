import numpy as np

class Pixels2MetresConverter:

    @staticmethod
    def ConvertProcessing(items_data: np.array, camResolution: np.array, 
    camFieldOfView, camHeight, camAzimut):
        items_coords_image = Pixels2MetresConverter.__centralizeCoordsItems(items_data)
        items_coords_metres = Pixels2MetresConverter.__convertPixels2Metres(items_coords_image,
        camResolution, camFieldOfView, camHeight)
        return Pixels2MetresConverter.__applyAzimutTranformation(items_coords_metres, camAzimut)


    def __centralizeCoordsItems(items_data: np.array):
        centralize_coords = np.array()
        for item in items_data:
            centralize_coords = np.append(centralize_coords, 
            [(item[0] + item[2])//2, (item[1] + item[3])//2])
        return centralize_coords

    def __convertPixels2Metres(centralize_coords: np.array,
     camResolution: np.array, camFieldOfView, camHeight):
        centralize_coords[:, 0] = centralize_coords[:, 0] / (camResolution[1]/2)
        centralize_coords[:, 1] = -centralize_coords[:, 1] / (camResolution[1]/2)
        centralize_coords *= camHeight * np.tan(camFieldOfView/2 * np.pi/180)
        centralize_coords[0] *= 16/9
        return centralize_coords

    def __applyAzimutTranformation(coords_metres: np.array, camAzimut):
        return coords_metres

        