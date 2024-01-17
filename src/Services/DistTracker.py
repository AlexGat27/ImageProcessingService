from src.Middlewares.IOUHandler import IOUHandler

class DistTracker:
    IOU_UP = 0.5
    STRIDE_UPDATE = 10

    def __init__(self):
        self.bbox_ids = {}
        self.id_count = 0
        self.stride = self.STRIDE_UPDATE

    def update(self, object_rect):
        objects_bbs_ids = []
        for rect in object_rect:
            x1, y1, x2, y2 = rect

            same_object_detected = False
            for id, pt in self.bbox_ids.items():
                iou = IOUHandler.IntersectionOverUnion(rect, pt)
                if iou > self.IOU_UP:
                    self.bbox_ids[id] = (x1, y1, x2, y2)
                    objects_bbs_ids.append([x1, y1, x2, y2, id])
                    same_object_detected = True
                    break

            if same_object_detected is False:
                self.bbox_ids[self.id_count] = (x1, y1, x2, y2)
                objects_bbs_ids.append([x1, y1, x2, y2, self.id_count])
                self.id_count += 1

        if self.stride < 0:
            new_bbox_ids = {}
            for obj_bb_id in objects_bbs_ids:
                _, _, _, _, object_id = obj_bb_id
                bbox_id = self.bbox_ids[object_id]
                new_bbox_ids[object_id] = bbox_id
            self.bbox_ids = new_bbox_ids.copy() 
            self.stride = self.STRIDE_UPDATE
        self.stride -= 1
        # print(self.bbox_ids)

        return objects_bbs_ids