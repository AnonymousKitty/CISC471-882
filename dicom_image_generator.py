import pydicom
import numpy as np
import cv2

class dicom_image_generator(object):

    def __init__(self, n, labels):
        self.n = [i.decode("utf-8") for i in n]
        self.labels = labels.astype('int32')
        print(self.labels[0], "uwu")        
        print(type(self.labels[0]), "uwu")
        self.num = 0
        self.image = self.load_image()
        print(self.image.dtype, self.image.shape, "y")


    def __iter__(self):
        return self


    # Python 3 compatibility
    def __next__(self):
        return self.next()
    
    def __call__(self):
        yield (self.image, self.labels[self.num])

    def load_image(self):
        dicom = pydicom.dcmread(self.n[self.num])
        pix_array = dicom.pixel_array
        img_normalized = cv2.normalize(pix_array, None, 0, 255, cv2.NORM_MINMAX)
        img_array = np.asarray(img_normalized).astype('float32')/255
        return img_normalized
    
    def next(self):
        if self.num < len(self.n):
            cur, self.num = self.num, self.num+1
            self.load_image()
            return cur
        raise StopIteration()

