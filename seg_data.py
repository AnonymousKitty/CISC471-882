import pydicom
import cv2

class Seg_Data():
    def __init__(self):
        self.full_dicoms = []
        self.ruids = []


    def import_dicoms(self, new_item):
        # load the seg and append it tp the full dicom list, in case there are multiple segs imported for some reason
        self.full_dicoms.append(pydicom.dcmread(new_item))
        # load in all the images according to the seg dicom
        # in case there are multiple segs imported for some reason, reset the dictionary of ruid : images
        self.ruids = []
        for dicom in self.full_dicoms:
            # find each frame and its ruid
            for frame in dicom.PerFrameFunctionalGroupsSequence:
                ruid = frame.DerivationImageSequence[0].SourceImageSequence[0].ReferencedSOPInstanceUID
                self.ruids.append(ruid)
                

    def load_images(self):
        images = []
        for dicom in self.full_dicoms:
            pix_array = dicom.pixel_array
            img_normalized = cv2.normalize(pix_array, None, 0, 255, cv2.NORM_MINMAX)
            # the segmentations shouldn't be rgb so we dont need to convert the channels
            for img in img_normalized:
                images.append(img)
        return images