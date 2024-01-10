import cv2
import numpy as np
from time import time

class CheckSimilarImagesService:
    def __init__(self):
        self.sift = cv2.SIFT_create()
        self.flanMatcher = cv2.FlannBasedMatcher()

    def __compare_images_with_perspective(self, image, imagePathsToCompare):

        gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keypoints1, descriptors1 = self.sift.detectAndCompute(gray_image1, None)

        for imgCompare_path in imagePathsToCompare:
            imageCompare = cv2.imread(imgCompare_path)
            gray_image2 = cv2.cvtColor(imageCompare, cv2.COLOR_BGR2GRAY)

            keypoints2, descriptors2 = self.sift.detectAndCompute(gray_image2, None)
            t = time()
            matches = np.array(self.flanMatcher.knnMatch(descriptors1, descriptors2, k=2))
            print(time()-t)
            vectorize_params = np.vectorize(lambda obj1, obj2: obj1.distance < obj2.distance * 0.75)
            good_matches = vectorize_params(matches[:,0], matches[:,1])
            if np.count_nonzero(good_matches==True)/len(good_matches) > 0.01: 
                return True
        return False
  
    def checkSimilarity(self, new_image_file, old_image_paths: list):
        new_image = cv2.imdecode(new_image_file, cv2.IMREAD_COLOR)
        h, w = new_image.shape[0], new_image.shape[1]
        if self.__compare_images_with_perspective(new_image, old_image_paths):
            return True
        return False
    