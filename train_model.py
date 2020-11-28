######################################################
# trains model to categorize rooms
######################################################

# load packages
import numpy as np
import os
import tensorflow as tf 
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from tensorflow.keras import layers 
from tensorflow.keras import Model
from tensorflow.keras.applications.vgg16 import VGG16
import matplotlib.pyplot as plt
from tensorflow import keras

# specify directories for train and validation
base_dir = 'data\\out\\'
model_dir = 'model\\'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')

# Add our data-augmentation parameters to ImageDataGenerator
train_datagen = ImageDataGenerator()
# Note that the validation data should not be augmented!
valid_datagen = ImageDataGenerator()

# Flow training images in batches of 20 using train_datagen generator
train_generator = train_datagen.flow_from_directory(
    directory = train_dir,
    target_size = (224, 224),
    color_mode = "rgb",
    batch_size = 32,
    class_mode = "binary",
    shuffle = True,
    seed = 42
)

# Flow validation images in batches of 20 using test_datagen generator
valid_generator = valid_datagen.flow_from_directory(
    directory = validation_dir,
    target_size = (224, 224),
    color_mode = "rgb",
    batch_size = 32,
    class_mode = "binary",
    shuffle = True,
    seed = 42
)

base_model = VGG16(
    input_shape = (224, 224, 3), # Shape of our images
    include_top = False, # Leave out the last fully connected layer
    weights = 'imagenet'
)

for layer in base_model.layers:
    layer.trainable = False

# Flatten the output layer to 1 dimension
x = layers.Flatten()(base_model.output)

# Add a fully connected layer with 512 hidden units and ReLU activation
x = layers.Dense(512, activation = 'relu')(x)

# Add a dropout rate of 0.5
x = layers.Dropout(0.5)(x)

# Add a final sigmoid layer for classification
x = layers.Dense(1, activation = 'sigmoid')(x)

model = tf.keras.models.Model(base_model.input, x)

model.compile(optimizer = tf.keras.optimizers.RMSprop(lr = 0.0001), loss = 'binary_crossentropy', metrics = ['acc'])

STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
STEP_SIZE_VALID=valid_generator.n//valid_generator.batch_size

vgghist = model.fit_generator(
    generator = train_generator, 
    validation_data = valid_generator, 
    validation_steps = STEP_SIZE_VALID,
    steps_per_epoch = STEP_SIZE_TRAIN, 
    epochs = 3
)

model.save(os.path.join(model_dir, 'model3'))

#evaluate model
model.summary()
plt.plot(vgghist.history["acc"])
plt.plot(vgghist.history['val_acc'])
plt.plot(vgghist.history['loss'])
plt.plot(vgghist.history['val_loss'])
plt.title("model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Accuracy","Validation Accuracy","loss","Validation Loss"])
plt.show()

model.evaluate_generator(
    generator = valid_generator,
    steps = STEP_SIZE_VALID
)

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

print(pred)
predicted_class_indices=np.argmax(pred, axis = 1)
print(predicted_class_indices)
labels = (train_generator.class_indices)
print(labels)
labels = dict((v,k) for k,v in labels.items())
predictions = [labels[k] for k in predicted_class_indices]
print(predictions)
