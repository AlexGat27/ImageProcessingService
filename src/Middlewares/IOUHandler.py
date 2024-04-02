import numpy as np

#Класс обработки Bounding box
class IOUHandler:

    @staticmethod
    def IntersectionOverUnion(boxA, boxB) -> float: #Метод рассчета пересечения bounding box
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

        iou = interArea / float(boxAArea + boxBArea - interArea)
        return iou #Возврат площади пересечения bounding box

    @staticmethod
    def RemoveInnerBoxes(boxes: np.array, ioulimit) -> np.array: #Метод удаления внутренних bounding box
        del_boxes_ids = [] #Массив id bounding box для удаления
        if boxes.shape[0] <= 1:
            return boxes    
        for i in range(boxes.shape[0] - 1):
            for j in range(i+1, boxes.shape[0]):
                iou = IOUHandler.IntersectionOverUnion(boxes[i], boxes[j]) #Рассчет пересечения областей
                if iou > ioulimit: #Если площадь больше максимальной, то рассчитать площадь обоих областей
                    area_i = (boxes[i][2] - boxes[i][0] + 1) * (boxes[i][3] - boxes[i][1] + 1)
                    area_j = (boxes[j][2] - boxes[j][0] + 1) * (boxes[j][3] - boxes[j][1] + 1)
                    
                    #Добавление индекса меньшей области
                    if area_i < area_j: 
                        del_boxes_ids.append(i)
                    else:
                        del_boxes_ids.append(j)
        boxes = np.delete(boxes, del_boxes_ids, axis=0) #Удаление лишних bounding box
        return boxes
    
    @staticmethod
    def RemoveSmallBigBoxes(boxes: np.array, imgShape: np.array, cropSquare) -> np.array: #Метод удаления слишком малых и слишком больших bounding box
        del_boxes_ids = []
        if boxes.shape[0] < 1:
            return boxes 
        for i in range(boxes.shape[0]):
            if (boxes[i][0] * boxes[i][1] / (imgShape[0]*imgShape[1])) > (1 - cropSquare) or \
            (boxes[i][0] * boxes[i][1] / (imgShape[0]*imgShape[1])) < cropSquare:
                del_boxes_ids.append(i)
        boxes = np.delete(boxes, del_boxes_ids, axis=0)
        return boxes

    @staticmethod
    def RemoveSmallCoefBoxes(boxes: np.array, confLim: float) -> np.array: #Метод удаления bounding box с малым коэфициентом уверенности
        del_boxes_ids = [] 
        for i, box in enumerate(boxes):
            if box[5] < confLim:
                del_boxes_ids.append(i)
        boxes = np.delete(boxes, del_boxes_ids, axis=0)
        return boxes