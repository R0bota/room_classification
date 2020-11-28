import cv2
import os
import fnmatch

# size of export images
size = (400, 400) 

print("OpenCV version:")
print(cv2.__version__)

# set path for import and export
dirPath = "/Users/maximilian/Desktop/img/"
prosPath = "/Users/maximilian/Desktop/img_pros/"
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