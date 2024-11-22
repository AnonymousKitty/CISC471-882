
import pydicom
import cv2

class Ct_Data:
    def __init__(self, res):
        self.dicoms = {}
        self.images = []
        

    def import_dicoms(self, new_item):
        item = pydicom.dcmread(new_item)
        uid = item.SOPInstanceUID
        self.dicoms[uid] = [item, self.load_images(item)]
    
    def load_images(self, dicom):
        pix_array = dicom.pixel_array
        img_normalized = cv2.normalize(pix_array, None, 0, 255, cv2.NORM_MINMAX)
        
        # ct images should be rgb so we need to create 3 channels
        img_rgb = cv2.merge([img_normalized, img_normalized, img_normalized])
        self.images.append(img_rgb)
        return img_rgb