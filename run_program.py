import os
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
import json
import patient_data
import cnn
from sklearn.metrics import classification_report, confusion_matrix


all_paths = json.loads(open("./paths.json").read())

personal_path = all_paths['personal_path']
non_cancerous_path = personal_path + all_paths['non_cancerous_path']
cancerous_path = personal_path + all_paths['cancerous_path']

# Using the patient_data data structure, load in all the patient data and save it in a dictionary with the folder name as the key
def load_all_patients(path):
    patients = {}
    folder = os.listdir(path)
    for name in folder:
        patients[name] = patient_data.Patient(os.path.join(path, name))
    return patients

def label_cancerous(patients):
    for patient in patients.values():
        patient.label_imgs()

nc_patients = load_all_patients(non_cancerous_path)
c_patients = load_all_patients(cancerous_path)
label_cancerous(c_patients)

# # not sure if we need this
# # create a list for the merged data
# x = []
# y = []

# create a list for only the cancerous dataset data
x_c = []
y_c = []
# create a list for only the non-cancerous dataset data
x_nc = []
y_nc = []

for patient in c_patients.values():
    for i, img in enumerate(patient.ct.images):
        x_c.append(img)
        y_c.append(patient.labels[i])
        # # not sure if we need this
        # x.append(img)
        # y.append(patient.labels[i])

for patient in nc_patients.values():
    for i, img in enumerate(patient.ct.images):
        x_nc.append(img)
        y_nc.append(patient.labels[i])
        # # not sure if we need this
        # x.append(img)
        # y.append(patient.labels[i])

# # not sure if we need this
# # Shuffle the merged data
# combined = list(zip(x, y))
# np.random.shuffle(combined)
# x2, y2 = zip(*combined)

def generate_train_test():
    # to ensure equal distribution of non-cancer to cancer data, split the data before merging it
    x_train, x_test, y_train, y_test = train_test_split(x_c, y_c, test_size=0.2, random_state=42)
    x_train_add, x_test_add, y_train_add, y_test_add = train_test_split(x_nc, y_nc, test_size=0.2, random_state=42)
    x_train.extend(x_train_add) 
    x_test.extend(x_test_add) 
    y_train.extend(y_train_add) 
    y_test.extend(y_test_add) 

x_train, x_test, y_train, y_test = generate_train_test()

# Assuming y_train and y_test are your labels for the train and test sets
train_class_distribution = pd.Series(y_train).value_counts(normalize=True)
test_class_distribution = pd.Series(y_test).value_counts(normalize=True)

print(f"Class distribution in training set:")
print(train_class_distribution)
print(f"\nClass distribution in testing set:")
print(test_class_distribution)

num_tests = 1
cnns = []
for i in range(num_tests):
    x_train, x_test, y_train, y_test = generate_train_test()
    cnns.append(cnn.CNN(x_train, x_test, y_train, y_test))

print(cnns[0].test_acc)
# Classification report
print(classification_report(cnns[0].y_test, cnns[0].y_pred))
# Confusion matrix
print(confusion_matrix(cnns[0].y_test, cnns[0].y_pred))