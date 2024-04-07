import cv2
import numpy as np

class CheckSimilarImages:
    def __init__(self):
        self.sift = cv2.SIFT_create()
        self.flanMatcher = cv2.FlannBasedMatcher()

    def _compare_images_with_perspective(self, image, imagePathsToCompare):

        gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keypoints1, descriptors1 = self.sift.detectAndCompute(gray_image1, None)

        for imgCompare_path in imagePathsToCompare:
            imageCompare = cv2.imread(imgCompare_path)
            gray_image2 = cv2.cvtColor(imageCompare, cv2.COLOR_BGR2GRAY)
            keypoints2, descriptors2 = self.sift.detectAndCompute(gray_image2, None)
            matches = np.array(self.flanMatcher.knnMatch(descriptors1, descriptors2, k=2))
            # print(descriptors2)
            vectorize_params = np.vectorize(lambda obj1, obj2: obj1.distance < obj2.distance * 0.75)
            good_matches = vectorize_params(matches[:,0], matches[:,1])
            print(np.count_nonzero(good_matches==True)/len(good_matches))
            if np.count_nonzero(good_matches==True)/len(good_matches) > 0.2: 
                return True
        return False
  
    def CheckSimilarity(self, new_image_file, old_image_paths: list):
        new_image = cv2.imdecode(new_image_file, cv2.IMREAD_COLOR)
        print(new_image)
        h, w = new_image.shape[0], new_image.shape[1]
        if self._compare_images_with_perspective(new_image, old_image_paths):
            return True
        return False
    