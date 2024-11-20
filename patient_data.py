import ct_data
import seg_data
import os
import cv2
from copy import deepcopy

class Patient:
    def __init__(self, path, resolution = (512, 512)):
        # in case you want to modify the resolution, the option exists. myst be a tuple of 2 ints though
        if len(resolution) != 2 or type(resolution[0]) != int or type(resolution[1]) != int:
            raise IndexError("Resolution must be a tuple of 2 integer values")
        self.path = path
        self.ct = ct_data.Ct_Data(resolution)
        self.seg = seg_data.Seg_Data(resolution)
        self.overlay = []
        self.load_data(self.path)
        # automatically assume this group is non cancerous
        self.labels = [0] * len(self.ct.images)
        self.overall = 0

    
    def load_data(self, folder_path):
        folder = os.listdir(folder_path)
        folder_size = len(folder)
        # go through each item in the folder
        for file_name in folder:
            # create a string with the path to the item being observed
            path = os.path.join(folder_path, file_name)
            # check if this is a ct file (folder will have multiple files and this file will be a dcm)
            if folder_size > 1 and file_name.endswith(".dcm"):
                self.ct.import_dicoms(path)
            # check if this is an annotation file (folder should only have 1 file which will be a dcm)
            elif folder_size == 1 and file_name.endswith(".dcm"):
                self.seg.import_dicoms(path)
            # check if this is folder, if so go into the folder
            elif os.path.isdir(path):
                self.load_data(path)

    def save_data_as_images(self, path):
        ct_folder = path + "/ct"
        seg_folder = path + "/segmentations"
        # make sure there is a folder for the images if one does not already exist
        if not os.path.exists(ct_folder):
            os.makedirs(ct_folder)
        if not os.path.exists(seg_folder):
            os.makedirs(seg_folder)
        # save images
        for i, img in enumerate(self.ct.images):
            cv2.imwrite(f"{ct_folder}/image_{i}.jpg", img)
        for i, img in enumerate(self.seg.images):
            cv2.imwrite(f"{seg_folder}/image_{i}.jpg", img)

    def overlay_seg_on_ct(self, output_folder = None, color_options = [[255,0,0],[0,255,0],[0,0,255]]):
        # local function to annotate images
        def annotate(image, annotation, color):
            img = image
            for x, row in enumerate(annotation):
                for y, col in enumerate(row):
                    # if there is an annotation here, there will be a value > 0
                    if col > 0:
                        img[x,y] = color
            return img

        for i in color_options:
            if len(i) != 3:
                raise IndexError("color options must be a list of 3 values from 0 to 255")
        overlay = []
        # make a deep copy of the cts so we don't mess up the originals. value[1] will be the images
        copied_dicoms = deepcopy(self.ct.dicoms)
        # make sure the output folder exists
        if output_folder:
            path = output_folder + "/overlays"
            if not os.path.exists(path):
                os.makedirs(path)
        # itterate through all the referenced uids 
        for i, ref_id in enumerate(self.seg.dicoms.keys()):
            # add the original image to the list of overlayed imaged
            overlay.append(copied_dicoms[ref_id][1])
            # itterate through each segmentation frame that references this uid and add the annotation to the image
            for j, seg in enumerate(self.seg.dicoms[ref_id]):
                color = color_options[j%len(color_options)]
                img = overlay[i]
                overlay[i] = annotate(img, seg, color)
            # if an output path was provided, save the completed image to this path
            if output_folder:
                cv2.imwrite(f"{path}/image_{i}.jpg", overlay[i])

    def label_imgs(self):
        self.labels = []
        self.overall = 0
        for uid in self.ct.dicoms.keys():
            if uid in self.seg.dicoms:
                self.labels.append(1)
                self.overall = 1
            else:
                self.labels.append(0)
