import numpy as np

class IOUHandler:

    @staticmethod
    def IntersectionOverUnion(boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

        iou = interArea / float(boxAArea + boxBArea - interArea)
        return iou

    @staticmethod
    def RemoveSmallBoxes(boxes: np.array, ioulimit):
        if boxes.shape[0] <= 1:
            return boxes    
        for i in range(boxes.shape[0] - 1):
            for j in range(i+1, boxes.shape[0]):
                iou = IOUHandler.IntersectionOverUnion(boxes[i], boxes[j])
                print("IOU: " + str(iou))
                if iou > ioulimit:
                    area_i = (boxes[i][2] - boxes[i][0] + 1) * (boxes[i][3] - boxes[i][1] + 1)
                    area_j = (boxes[j][2] - boxes[j][0] + 1) * (boxes[j][3] - boxes[j][1] + 1)
                    
                    if area_i < area_j:
                        boxes = np.delete(boxes, (i), axis=0)
                    else:
                        boxes = np.delete(boxes, (j), axis=0)
        return boxes