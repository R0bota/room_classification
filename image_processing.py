import cv2
import os
import fnmatch
import yaml
import os.path
from os import path
from random import random

#load config file
with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

    mainPath = data["mainPath"]
    trainPath = data["trainPath"]
    validationPath = data["validationPath"]
    ratioTtoV = data["ratioTtoV"]
    imageType = data["imageType"]
    size = (data["imageWidth"], data["imageHeight"])

#check if directory exists
print("main path exists: " + str(path.isdir(mainPath)))
if(path.exists(mainPath) == False):
    exit()

if(mainPath.endswith("/")== False):
    mainPath = mainPath + "/"



def listdirs(p):
    return [d for d in os.listdir(p) if os.path.isdir(os.path.join(p, d)) and d.startswith(".") == False]

def listfiles(p):
    return [d for d in os.listdir(p) if os.path.isfile(os.path.join(p, d)) and d.startswith(".") == False]


listOfDir = listdirs(mainPath)    
print("Folders found in main directory: " + str(listOfDir))

print("search for " + imageType + "-files")
pattern = "*." + imageType





# loop over each subfolder
for dir in listOfDir:
    print("current directory:" + dir)

    # check if export directory has right structure
    print("Path Vali exist"  + str(os.path.exists(validationPath + dir)))
    if(os.path.exists(validationPath + dir) == False):
        #create dir
        os.mkdir(validationPath + dir)

    if(os.path.exists(trainPath + dir) == False):
        #create dir
        os.mkdir(trainPath + dir)

    #get files in directory
    listOfFiles = listfiles(mainPath + dir)
    print(listOfFiles)

    for file_name in listOfFiles:
        path = mainPath + dir + "/" + file_name
        
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        resized = cv2.resize(gray, size, interpolation = cv2.INTER_AREA)
        
        #check if export folder exist
        if random() > ratioTtoV:
            path = validationPath + dir + "/" + file_name
        else:
            path = trainPath + dir + "/" + file_name
        
        cv2.imwrite(path, resized)

