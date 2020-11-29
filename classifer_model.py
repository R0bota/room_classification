import glob
from keras.preprocessing import image
import keras,os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from keras.applications.vgg16 import decode_predictions

base_dir = 'data\\'
model_dir = 'model\\'
train_dir = os.path.join(base_dir, 'train')
out_dir = os.path.join(base_dir, 'out_test')

model = keras.models.load_model(os.path.join(model_dir, 'model4'))

train_datagen = ImageDataGenerator()
train_generator = train_datagen.flow_from_directory(
    directory = out_dir,
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

pics = (glob.glob(base_dir + 'out_test\\' + '*.png'))
i = 1
for pic in pics:
    img = tf.keras.preprocessing.image.load_img(pic, target_size=(224, 224))
    imgs = np.asarray(img)
    img = np.expand_dims(imgs, axis = 0)

    output = model.predict(img, batch_size = 1)
    predicted_class_indices = np.argmax(output, axis = 1)
    predictions = [labels[k] for k in predicted_class_indices]
    print(output[0][predicted_class_indices])

    if output[0][predicted_class_indices] > 0.99:
        print(pic + " is " + str(predictions[0]))
        os.rename(pic, base_dir + 'out_test\\' + output[0][predicted_class_indices] + i)
        i += 1
