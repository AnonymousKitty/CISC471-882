import pydicom
import cv2

class Seg_Data():
    def __init__(self, res):
        self.full_dicoms = []
        self.dicoms = {}
        self.images = []
     


    def import_dicoms(self, new_item):
        # load the seg and append it tp the full dicom list, in case there are multiple segs imported for some reason
        self.full_dicoms.append(pydicom.dcmread(new_item))
        # load in all the images according to the seg dicom
        self.load_images()
        # in case there are multiple segs imported for some reason, reset the dictionary of ruid : images
        self.dicoms = {}
        for dicom in self.full_dicoms:
            # find each frame and its ruid
            for i, frame in enumerate(dicom.PerFrameFunctionalGroupsSequence):
                ruid = frame.DerivationImageSequence[0].SourceImageSequence[0].ReferencedSOPInstanceUID
                # if the ruid has already been added, add the image to the list associated with this ruid
                if ruid in self.dicoms.keys():
                    self.dicoms[ruid].append(self.images[i])
                # if the ruid doesnt exist, add it and put the image in
                else:
                    self.dicoms[ruid] = []
                    self.dicoms[ruid].append(self.images[i])

    def load_images(self):
        self.images = []
        for dicom in self.full_dicoms:
            pix_array = dicom.pixel_array
            img_normalized = cv2.normalize(pix_array, None, 0, 255, cv2.NORM_MINMAX)
            # the segmentations shouldn't be rgb so we dont need to convert the channels
            for img in img_normalized:
                self.images.append(img)