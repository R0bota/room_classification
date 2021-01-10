######################################################
# score images which are already classified to check
# model quality and plot certain plots to assess
# accuracy of classification
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
import plotly.express as px
import seaborn as sns
import matplotlib as mpl
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from keras.applications.vgg16 import decode_predictions
from itertools import chain
from datetime import datetime
from sys import platform
from bokeh.plotting import output_file, show

print(tf.__version__)

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)

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

# specify which category to check with which threshold of confidence
pic_cat = 'sleeping_room'
th = 0.9

#load model
model = keras.models.load_model(os.path.join(model_dir, model_id))
dbfile = open(model_dir + model_id + '.pkl', 'rb')      
labels = pickle.load(dbfile) 
dbfile.close()

# read files to score
pics = (glob.glob(data_dir + 'classified\\' + pic_cat + sep + '*.png'))

# variable setup for model results
sc = []
cat = []
pic_id = []

for pic in pics:

    # which image is currently scored
    print(pic[(len(data_dir + 'classified\\' + pic_cat + sep)):(len(pic)-4)])

    # preprocess image
    img = tf.keras.preprocessing.image.load_img(pic, target_size=(224, 224))
    imgs = np.asarray(img)
    img = np.expand_dims(imgs, axis = 0)

    # score image
    output = model.predict(img, batch_size = 1)
    predicted_class_indices = np.argmax(output, axis = 1)
    predictions = [labels[k] for k in predicted_class_indices]

    # only classify if over specified threshold
    if output[0][predicted_class_indices] < th:
        predictions[0] = 'unsure'
    
    # file arrays
    sc.append(output[0][predicted_class_indices])
    cat.append(predictions[0])
    pic_id.append(pic[(len(data_dir + 'classified\\' + pic_cat + sep)):(len(pic)-4)])

# create result dataframe
model_res = pd.DataFrame(pic_id)
model_res['predicted_category'] = pd.DataFrame(cat)
model_res['true_category'] = pic_cat
model_res['score'] = pd.DataFrame(sc)
model_res.columns = ['pic_id', 'predicted_category', 'true_category', 'score']

# save results to csv for jupyter
#res.to_csv(data_dir + 'sample_results.csv')

# check df
print(model_res.head())
print(model_res.score.describe())
print(model_res.predicted_category.value_counts())

# plotly theme
template = 'plotly_dark' 

# confusion matrix
confusion_matrix = pd.crosstab(model_res['true_category'], model_res['predicted_category'], 
                               rownames = ['Actual'], colnames = ['Predicted'], margins = False)

sns.heatmap(confusion_matrix, annot = True, cbar = False)
plt.show()

# plot score distribution
fig = px.violin(model_res, y = "score", x = "true_category", box = True, points = "all",
          hover_data = ['pic_id'], template = template)
fig.show()

# plot score distribution over different categories plotly
fig = px.violin(model_res, y = "score", x = "predicted_category", color = "predicted_category", 
                box = True, points = "all", hover_data = ['pic_id'], template = template)
fig.show()