# CISC471-882
## Description
Project on developing a survival model based on binary cancer classification of lymph nodes CT images

## Datasets 
This project uses the Images/Segmentation data found in the following TCIA repositories:

#### Non-cancerous lymph node CTs with annotations:
https://www.cancerimagingarchive.net/collection/ct-lymph-nodes/

#### Pan-cancerous lymph node CTs with annotations:
https://www.cancerimagingarchive.net/collection/mediastinal-lymph-node-seg/

## Imports/installations
This project uses Python and Anaconda 

### Python Installation Guide
* Install python (https://www.python.org/downloads/)

### Anaconda Installation Guide
* Install anaconda (https://anaconda.org/)
* Open **Anaconda Prompt**
* Create an environment using ```conda create --name <env-name>``` 
* Activate the environment using ```conda activate <env-name>``` 
* Install required packages in the environment

### Required Packages
To install all the required packages, run the following in your command line:

```
pip install pydicom opencv-python numpy scikit-learn pandas
```

Individually, all the imports required are:

* pydicom --> ```pip install pydicom```
* os --> standard library
* cv2 --> ```pip install opencv-python```
* numpy --> ```pip install numpy```
* sklearn --> ```pip install scikit-learn```
* pandas --> ```pip install pandas```
