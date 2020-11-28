import os
import tensorflow as tf 
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from tensorflow.keras import layers 
from tensorflow.keras import Model 
import matplotlib.pyplot as plt

base_dir = 'data\\out\\'
bath_dir = os.path.join(base_dir, 'bath_room')
empty_dir = os.path.join(base_dir, 'empty_room')

# Directory with our training cat pictures
bath_train_dir = os.path.join(bath_dir, 'train')

# Directory with our training dog pictures
empty_train_dir =  os.path.join(empty_dir, 'train')

# Directory with our validation cat pictures
empty_validation_dir = os.path.join(bath_dir, 'validation')

# Directory with our validation dog pictures
bath_validation_dir = os.path.join(empty_dir, 'validation')

# Set up matplotlib fig, and size it to fit 4x4 pics
import matplotlib.image as mpimg
nrows = 4
ncols = 4

fig = plt.gcf()
fig.set_size_inches(ncols*4, nrows*4)
pic_index = 100
train_cat_fnames = os.listdir( bath_train_dir )
train_dog_fnames = os.listdir( empty_train_dir )


next_cat_pix = [os.path.join(bath_train_dir, fname) 
                for fname in train_cat_fnames[ pic_index-8:pic_index] 
               ]

next_dog_pix = [os.path.join(empty_train_dir, fname) 
                for fname in train_dog_fnames[ pic_index-8:pic_index]
               ]

for i, img_path in enumerate(next_cat_pix+next_dog_pix):
  # Set up subplot; subplot indices start at 1
  sp = plt.subplot(nrows, ncols, i + 1)
  sp.axis('Off') # Don't show axes (or gridlines)

  img = mpimg.imread(img_path)
  plt.imshow(img)

plt.show()