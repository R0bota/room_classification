import glob
from keras.preprocessing import image
import keras,os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from keras.applications.vgg16 import decode_predictions
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

base_dir = 'data' + sep
model_dir = 'model' + sep
train_dir = os.path.join(base_dir, 'train')
out_dir = os.path.join(base_dir, 'out_test')

model = keras.models.load_model(os.path.join(model_dir, 'model4'))

train_datagen = ImageDataGenerator()
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

pics = (glob.glob(base_dir + 'out_test' + sep + '*.png'))
i = 1
for pic in pics:
    print(pic)
    img = tf.keras.preprocessing.image.load_img(pic, target_size=(224, 224))
    imgs = np.asarray(img)
    img = np.expand_dims(imgs, axis = 0)

    output = model.predict(img, batch_size = 1)
    predicted_class_indices = np.argmax(output, axis = 1)
    predictions = [labels[k] for k in predicted_class_indices]
    print(output[0][predicted_class_indices])

    if output[0][predicted_class_indices] > 0.99:
        print(pic + " is " + str(predictions[0]))
        #print(base_dir + 'out_test' + sep + str(predictions[0]) + str(i) + '.png')
        os.rename(pic, base_dir + 'out_test' + sep + str(predictions[0]) + str(i) + '.png')
        i += 1
