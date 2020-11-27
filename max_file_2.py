import cv2

size = (400, 400)

print("OpenCV version:")
print(cv2.__version__)

print("Load image")
img = cv2.imread("/Users/maximilian/Desktop/Test_Bild.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

height, width = img.shape[:2]
print("image has width of " + str(width) + " and height of " + str(height))

cv2.imshow("grayscale Image", gray)

cv2.imwrite("/Users/maximilian/Desktop/Test_Bild_gray.jpg", gray) 

resized = cv2.resize(gray, size, interpolation = cv2.INTER_AREA)
cv2.imwrite("/Users/maximilian/Desktop/Test_Bild_gray.jpg", resized) 


#cv2.waitKey(0)
#cv2.destroyAllWindows()