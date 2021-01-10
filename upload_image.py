import base64
import os
from urllib.parse import quote as urlquote

from flask import Flask, send_from_directory
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import glob
import pickle
import keras
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
#import seaborn as sns
import matplotlib as mpl
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from keras.applications.vgg16 import decode_predictions
from itertools import chain
from datetime import datetime
from sys import platform
from bokeh.plotting import output_file, show

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

# specify directory paths
data_dir = 'data\\'
model_dir = 'model\\'
model_id = '2020-11-29_12-46-54_144487'
UPLOAD_DIRECTORY = "assets"

# specify threshold of confidence
th = 0.9

#load model
model = keras.models.load_model(os.path.join(model_dir, model_id))
dbfile = open(model_dir + model_id + '.pkl', 'rb')      
labels = pickle.load(dbfile) 
dbfile.close()



if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files direct
server = Flask(__name__)
app = dash.Dash(server=server)


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


app.layout = html.Div(
    [
        html.H1("Room Classifier"),
        html.H3("Upload"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        ),
        html.H3("Zu klassifizieren:"),
        html.Ul(id="file-list", style={"list-style-type": "none"}),
        html.H3("Ergebnis:"),
        html.Div(["Küche"])
    ],
    style={"max-width": "500px"},
)


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    print("save to: " + os.path.join(UPLOAD_DIRECTORY, name))
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))
    # Classify the file
    classifyImg()


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    print(files)
    if len(files) == 0:
        return [html.Li("Nothing to classify...!")]
    else:
        # Display lst file of files array
        return [html.Li(html.Img(src=app.get_asset_url(files[len(files) - 1])))]

def classifyImg():
    #function to classify image
    print("classify uploaded Image")
    sc = []
    cat = []
    pic_id = []
    #pic = (glob.glob(UPLOAD_DIRECTORY + '\\' + '*.png'))
    pics = (glob.glob(UPLOAD_DIRECTORY + '\\' + 'img_2vpyz4u_19.png'))
    for pic in pics:
        img = tf.keras.preprocessing.image.load_img(pic, target_size=(224, 224))
        imgs = np.asarray(img)
        img = np.expand_dims(imgs, axis = 0)
        print("predict image")
        # score image
        output = model.predict(img, batch_size = 1)
        predicted_class_indices = np.argmax(output, axis = 1)
        predictions = [labels[k] for k in predicted_class_indices]

        # only classify if over specified threshold
        if output[0][predicted_class_indices] < th:
            predictions[0] = 'unsure'
            # variable setup for model results
    
        print(predictions[0])





if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
