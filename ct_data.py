
import pydicom
import numpy as np
import cv2

class Ct_Data:
    def __init__(self):
        self.data = {}

    def import_dicoms(self, new_item):
        item = pydicom.dcmread(new_item)
        uid = item.SOPInstanceUID
        img = self.load_images(item)
        self.data[uid] = img
    
    def load_images(self, dicom):
        pix_array = dicom.pixel_array
        img_normalized = cv2.normalize(pix_array, None, 0, 255, cv2.NORM_MINMAX)
        img_array = np.asarray(img_normalized).astype('float32')/255
        return img_normalized