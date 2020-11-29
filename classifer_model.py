import glob
from keras.preprocessing import image
import keras,os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from keras.applications.vgg16 import decode_predictions
from sys import platform
import os
import pickle

#check OS
print("Checking OS...")
if platform == "linux" or platform == "linux2":
    print("You`re using Linux")
elif platform == "darwin":
    print("You`re using MacOS")
    sep = '/'
elif platform == "win32":
    print("You`re using Windows")
    sep = '\\'

def listfiles(p):
    return [d for d in os.listdir(p) if os.path.isfile(os.path.join(p, d)) and d.startswith(".") == False]


base_dir = 'data' + sep
model_dir = 'model' + sep

out_dir = os.path.join(base_dir, 'out_test')

model_id = '2020-11-29_12-46-54_144487'

model = keras.models.load_model(os.path.join(model_dir, model_id))

dbfile = open(model_dir + model_id + '.pkl', 'rb')      
labels = pickle.load(dbfile) 
dbfile.close()

pics = (glob.glob(base_dir + 'out_test' + sep + '*.png'))
for pic in pics:
    print(pic)
    pic_name = os.path.basename(pic)
    
    img = tf.keras.preprocessing.image.load_img(pic, target_size=(224, 224))
    imgs = np.asarray(img)
    img = np.expand_dims(imgs, axis = 0)

    output = model.predict(img, batch_size = 1)
    predicted_class_indices = np.argmax(output, axis = 1)
    predictions = [labels[k] for k in predicted_class_indices]
    print(output[0][predicted_class_indices])

    if output[0][predicted_class_indices] > 0.99:
        print(pic + " is " + str(predictions[0]))
        print(base_dir + 'out_test' + sep + str(predictions[0]) + '_' + pic_name)
        os.rename(pic, base_dir + 'out_test' + sep + str(predictions[0]) + '_' + pic_name)
