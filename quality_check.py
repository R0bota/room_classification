######################################################
# score images which are already classified to check
# model quality
######################################################

# load packages
import glob
import os
import keras
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from keras.applications.vgg16 import decode_predictions

# specify directory paths
data_dir = 'data\\'
model_dir = 'model\\'
#train_dir = os.path.join(base_dir, 'train')

model = keras.models.load_model(os.path.join(model_dir, 'model4'))

print(model.predict_classes)

""" train_datagen = ImageDataGenerator()
train_generator = train_datagen.flow_from_directory(
    directory = train_dir,
    target_size = (224, 224),
    color_mode = "rgb",
    batch_size = 32,
    class_mode = "categorical",
    shuffle = True,
    seed = 42
)
labels = (train_generator.class_indices)
labels = dict((v,k) for k,v in labels.items())
print(labels)

pics = (glob.glob(base_dir + 'test\\' + '*.png')) """