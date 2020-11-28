import cv2
import os
import fnmatch
import yaml

import os.path
from os import path

#load config file
with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

    # size of export images
    size = (data["imageWidth"], data["imageHeight"])
    print("size of processed images :")
    print(size)

# set path for import and export path
dirPath = input("Import path : ")
prosPath = input("Export path: ")

# add / if nessassary
if(dirPath.endswith("/")== False):
    dirPath = dirPath + "/"

if(prosPath.endswith("/")== False):
    prosPath = prosPath + "/"

#check if directory exists
print("Path exists: " + str(path.exists('dirPath')))
if(path.exists('dirPath') == False or path.exists('prosPath') == False):
    print("Path not found")
    exit()

listOfFiles = os.listdir(dirPath)
pattern = "*.jpg"

# loop over files
for name in listOfFiles:
    if fnmatch.fnmatch(name, pattern):
        print(name)
        path = dirPath + name
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        height, width = img.shape[:2]
        print("image has width of " + str(width) + " and height of " + str(height))
        
        path = prosPath + name
        resized = cv2.resize(gray, size, interpolation = cv2.INTER_AREA)
        cv2.imwrite(path, resized)

print("done")