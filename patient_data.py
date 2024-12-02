import ct_data
import os
import pydicom

class Patient:
    def __init__(self, path):
        self.ct = ct_data.Ct_Data()
        self.segpath = None
        self.load_data(path)
        # automatically assume this group is non cancerous
        self.labels = [0] * len(self.ct.data)
    
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
                self.segpath = path
            # check if this is folder, if so go into the folder
            elif os.path.isdir(path):
                self.load_data(path)

    def label_imgs(self):
        self.labels = []
        ruidlist = []
        full_dicom = pydicom.dcmread(self.segpath)
        # load in all the images according to the seg dicom
        for frame in full_dicom.PerFrameFunctionalGroupsSequence:
            ruid = frame.DerivationImageSequence[0].SourceImageSequence[0].ReferencedSOPInstanceUID
            ruidlist.append(ruid)
        for uid in self.ct.data.keys():
            if uid in ruidlist:
                self.labels.append(1)
            else:
                self.labels.append(0)

    # removing the following 2 functions to try to save memory

    # # function that allows users to visualize data
    # def save_data_as_images(self, path):
    #     ct_folder = path + "/ct"
    #     seg_folder = path + "/segmentations"
    #     # make sure there is a folder for the images if one does not already exist
    #     if not os.path.exists(ct_folder):
    #         os.makedirs(ct_folder)
    #     if not os.path.exists(seg_folder):
    #         os.makedirs(seg_folder)
    #     # save images
    #     for i, img in enumerate(self.ct.images):
    #         cv2.imwrite(f"{ct_folder}/image_{i}.jpg", img)
    #     for i, img in enumerate(self.seg.images):
    #         cv2.imwrite(f"{seg_folder}/image_{i}.jpg", img)

    # # function that allows users to see annotations on top of cts
    # def overlay_seg_on_ct(self, output_folder = None, color_options = [[255,0,0],[0,255,0],[0,0,255]]):
    #     # local function to annotate images
    #     def annotate(image, annotation, color):
    #         img = image
    #         for x, row in enumerate(annotation):
    #             for y, col in enumerate(row):
    #                 # if there is an annotation here, there will be a value > 0
    #                 if col > 0:
    #                     img[x,y] = color
    #         return img

    #     for i in color_options:
    #         if len(i) != 3:
    #             raise IndexError("color options must be a list of 3 values from 0 to 255")
    #     overlay = []
    #     # make a deep copy of the cts so we don't mess up the originals. value[1] will be the images
    #     copied_dicoms = deepcopy(self.ct.dicoms)
    #     # make sure the output folder exists
    #     if output_folder:
    #         path = output_folder + "/overlays"
    #         if not os.path.exists(path):
    #             os.makedirs(path)
    #     # itterate through all the referenced uids 
    #     for i, ref_id in enumerate(self.seg.dicoms.keys()):
    #         # add the original image to the list of overlayed imaged
    #         overlay.append(copied_dicoms[ref_id][1])
    #         # itterate through each segmentation frame that references this uid and add the annotation to the image
    #         for j, seg in enumerate(self.seg.dicoms[ref_id]):
    #             color = color_options[j%len(color_options)]
    #             img = overlay[i]
    #             overlay[i] = annotate(img, seg, color)
    #         # if an output path was provided, save the completed image to this path
    #         if output_folder:
    #             cv2.imwrite(f"{path}/image_{i}.jpg", overlay[i])
