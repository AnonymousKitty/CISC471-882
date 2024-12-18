# CISC471-882
### Authors: Catarina Borges McDiarmid, Mide Olanrewaju & Shrinidhi Thatahngudi Sampath Krishnan

## Description
CISC 471/882 final project on developing a binary cancer classification computer neural network (CNN) model to classify mediastinal lymph nodes using CT images.

## Datasets 
This project uses the images and segmentation data found in the following TCIA repository:

#### Pan-cancerous lymph node CTs with annotations:
https://www.cancerimagingarchive.net/collection/mediastinal-lymph-node-seg/

## Imports/installations
This project uses Python and Anaconda.

You can install python at https://www.python.org/downloads/

You can install Anaconda at https://anaconda.org/

### Anaconda environment setup
* Open **Anaconda Prompt**
* Create an environment using ```conda create --name <env-name> python==3.12.3``` 
* Activate the environment using ```conda activate <env-name>``` 
* Install required packages in the environment

### Required Packages
To install all the required packages, run the following in your command line:

```
pip install -r requirements.txt
```

Individually, all the imports required are:

* pydicom --> ```pip install pydicom```
* os --> standard library
* cv2 --> ```pip install opencv-python```
* numpy --> ```pip install numpy```
* sklearn --> ```pip install scikit-learn```
* json --> standard library
* tensorflow --> ```pip install tensorflow```
* keras --> ```pip install keras```

## License
Copyright (C) 2024 Catarina Borges McDiarmid, Mide Olanrewaju & Shrinidhi Thatahngudi Sampath Krishnan

See the [LICENSE](https://github.com/AnonymousKitty/CISC471-882/blob/cb98497733e0b3fb0a609d1be0c82fead46cd931/LICENSE.md) file for license rights and limitations (GNU General Public License family)
