import numpy as np

class Pixels2MetresConverter:

    @staticmethod
    def ConvertProcessing(item_data: np.array, camResolution: np.array, 
    camFieldOfView, camHeight, camAzimut):
        item_coords_image = Pixels2MetresConverter.__centralizeCoordsItems(item_data)
        item_coords_metres = Pixels2MetresConverter.__convertPixels2Metres(item_coords_image,
        camResolution, camFieldOfView, camHeight)
        items_coords_image_azumut = Pixels2MetresConverter.__applyAzimutTranformation(item_coords_metres, camAzimut)
        return items_coords_image_azumut


    def __centralizeCoordsItems(items_data: np.array):
        return np.array([(items_data[0]+items_data[2])//2, (items_data[1]+items_data[3])//2])

    def __convertPixels2Metres(centralize_coords: np.array,
     camResolution: np.array, camFieldOfView, camHeight):
        centralize_coords[0] = centralize_coords[0] / (camResolution[0]/2)
        centralize_coords[1] = -centralize_coords[1] / (camResolution[1]/2)
        centralize_coords *= camHeight * np.tan(camFieldOfView/2 * np.pi/180)
        centralize_coords[0] *= camResolution[0]/camResolution[1]
        return centralize_coords

    def __applyAzimutTranformation(coords_metres: np.array, camAzimut):
        radAzimut = -camAzimut * np.pi / 180
        x = coords_metres[0]
        y = coords_metres[1]
        coords_metres[0] = x * np.cos(radAzimut) - y * np.sin(radAzimut)
        coords_metres[1] = x * np.sin(radAzimut) + y * np.cos(radAzimut)
        return coords_metres

        