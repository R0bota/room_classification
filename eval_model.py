import glob
from keras.preprocessing import image
import keras,os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator 

base_dir = 'data\\out\\'
model_dir = 'model\\'

model = keras.models.load_model(os.path.join(model_dir, 'model2'))

pics = (glob.glob(base_dir + 'test\\' + '*.png'))

""" for pic in pics:
    img = tf.keras.preprocessing.image.load_img(pic, target_size=(224, 224))
    imgs = np.asarray(img)
    img = np.expand_dims(imgs, axis=0)
    output = model.predict(img, batch_size=1)
    print(output)
    if output[[0]] > 0.99:
        print(pic + " is an empty room")
        plt.imshow(imgs)
        plt.show()
    if output[[0]] < 0.00001:
        print(pic + " is a bath")
        plt.imshow(imgs)
        plt.show() """

test_datagen = ImageDataGenerator()

test_generator = test_datagen.flow_from_directory(
    directory = os.path.join(base_dir, 'test\\'),
    target_size = (224, 224),
    color_mode = "rgb",
    batch_size = 1,
    class_mode = None,
    shuffle = False,
    seed = 42
)

STEP_SIZE_TEST=test_generator.n//test_generator.batch_size

test_generator.reset()

pred = model.predict_generator(
    test_generator,
    steps = STEP_SIZE_TEST,
    verbose = 1
)

train_dir = os.path.join(base_dir, 'train')
train_datagen = ImageDataGenerator()
train_generator = train_datagen.flow_from_directory(
    directory = train_dir,
    target_size = (224, 224),
    color_mode = "rgb",
    batch_size = 32,
    class_mode = "binary",
    shuffle = True,
    seed = 42
)

print(pred)
predicted_class_indices=np.argmax(pred, axis = 1)
print(predicted_class_indices)
labels = (train_generator.class_indices)
print(labels)
labels = dict((v,k) for k,v in labels.items())
predictions = [labels[k] for k in predicted_class_indices]
print(predictions)