######################################################
# score images which are already classified to check
# model quality
######################################################

# load packages
import glob
import pickle
import os
import keras
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from keras.applications.vgg16 import decode_predictions
from itertools import chain
from datetime import datetime
from sys import platform

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

# specify directory paths
data_dir = 'data\\'
model_dir = 'model\\'
model_id = '2020-11-29_12-46-54_144487'

model = keras.models.load_model(os.path.join(model_dir, model_id))

dbfile = open(model_dir + model_id + '.pkl', 'rb')      
labels = pickle.load(dbfile) 
dbfile.close()

pics = (glob.glob(data_dir + 'classified\\corridor' + sep + '*.png'))

sc = []
cat = []

for pic in pics:

    print(pic)

    img = tf.keras.preprocessing.image.load_img(pic, target_size=(224, 224))
    imgs = np.asarray(img)
    img = np.expand_dims(imgs, axis = 0)

    output = model.predict(img, batch_size = 1)
    predicted_class_indices = np.argmax(output, axis = 1)
    predictions = [labels[k] for k in predicted_class_indices]
    
    sc.append(output[0][predicted_class_indices])
    cat.append(predictions[0])

res = pd.DataFrame(sc)
res['category'] = pd.DataFrame(cat)
res.columns = ['score', 'category']
print(res.score.describe())
print(res.category.value_counts())