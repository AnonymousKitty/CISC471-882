import os
import pydicom

class Patient:
    def __init__(self, path, name, has_seg = False):
        self.name = name
        self.ct_uids = []
        self.ct_paths = []
        self.has_seg = has_seg
        self.seg_path = None
        self.patient_path = os.path.join(path, name)
        self.load_data(self.patient_path)
        if self.ct_paths == []:
            # catch case where something went wrong with this filepath
            return
        if has_seg:
            self.label_imgs()
        # automatically assume this group is non cancerous
        else:
            self.labels = [0] * len(self.ct_uids)
    
    def load_data(self, curr_path):
        folder = os.listdir(curr_path)
        folder_size = len(folder)
        # go through each item in the folder
        for file_name in folder:
            # create a string with the path to the item being observed
            path = os.path.join(curr_path, file_name)
            # check if this is a ct file (folder will have multiple files and this file will be a dcm)
            if folder_size > 1 and file_name.endswith(".dcm"):
                self.ct_paths.append(path)
                item = pydicom.dcmread(path)
                uid = item.SOPInstanceUID
                self.ct_uids.append(uid)
            # check if this is an annotation file (folder should only have 1 file which will be a dcm)
            elif folder_size == 1 and file_name.endswith(".dcm") and self.has_seg:
                self.seg_path = path
            # check if this is folder, if so go into the folder
            elif os.path.isdir(path):
                self.load_data(path)

    def label_imgs(self):
        self.labels = []
        ruidlist = []
        full_dicom = pydicom.dcmread(self.seg_path)
        # load in all the images according to the seg dicom
        for frame in full_dicom.PerFrameFunctionalGroupsSequence:
            ruid = frame.DerivationImageSequence[0].SourceImageSequence[0].ReferencedSOPInstanceUID
            ruidlist.append(ruid)
        for uid in self.ct_uids:
            if uid in ruidlist:
                self.labels.append(1)
            else:
                self.labels.append(0)
