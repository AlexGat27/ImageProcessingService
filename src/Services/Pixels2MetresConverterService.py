import numpy as np

class Pixels2MetresConverter:

    @staticmethod
    def ConvertProcessing(items_data: np.array, camResolution: np.array, 
    camFieldOfView, camHeight, camAzimut):
        items_coords_image = Pixels2MetresConverter.__centralizeCoordsItems(items_data)
        items_coords_image_azumut = Pixels2MetresConverter.__applyAzimutTranformation(items_coords_image, camAzimut)
        return Pixels2MetresConverter.__convertPixels2Metres(items_coords_image_azumut,
        camResolution, camFieldOfView, camHeight)


    def __centralizeCoordsItems(items_data: np.array):
        centralize_coords = np.asarray([[0, 0]], float)
        for item in items_data:
            centralize_coords = np.vstack([centralize_coords, 
            [(item[0] + item[2])//2, (item[1] + item[3])//2]])
        return centralize_coords[1:]

    def __convertPixels2Metres(centralize_coords: np.array,
     camResolution: np.array, camFieldOfView, camHeight):
        for coord in centralize_coords:
            coord[0] = coord[0] / (camResolution[0]/2)
            coord[1] = -coord[1] / (camResolution[1]/2)
            coord *= camHeight * np.tan(camFieldOfView/2 * np.pi/180)
            coord[0] *= camResolution[0]/camResolution[1]
        return centralize_coords

    def __applyAzimutTranformation(coords_metres: np.array, camAzimut):
        radAzimut = camAzimut * np.pi / 180
        for coords in coords_metres:
            coords[0] = coords[0] * np.cos(radAzimut) - coords[1] * np.sin(radAzimut)
            coords[1] = coords[0] * np.sin(radAzimut) + coords[1] * np.cos(radAzimut)
        return coords_metres

        