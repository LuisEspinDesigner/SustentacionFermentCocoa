import numpy as np
import cv2
import os
import werkzeug
import flask
import imageio
import base64
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
import scipy.misc

from flask import Flask,jsonify, request
from flask.json import jsonify
from flask_cors import CORS, cross_origin
from PIL import Image
import io

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#MODELO

Length, Height = 156, 256

#CNN
cnn = load_model("model/ModelFermentedCocoaBean_Version10.h5") #CARGA EL MODELO CREADO 
cnn.load_weights("model/pesos_ModelFermentedCocoaBean_Version10.h5") #CARGA EL ARCHIVO DE PESOS CREADO

def predict2(file):
  x = load_img(file, target_size=(Length, Height))
  x = img_to_array(x)
  #DIMENSIONA
  x = np.expand_dims(x, axis=0)
  array = cnn.predict(x)
  result = array[0]
  answer = np.argmax(result)
  return answer


#APIS
app = Flask(__name__)

@app.route('/ping')
def ping():
    respapi = ''
    resp = predict2('G:/Unidades compartidas/Fermented_Cocoa_Bean/Archive/Training/Mediana_Fermentacion/48362448_362844227801513_150633410832891904_n.jpg')
    if resp == 0:
        respapi = 'Buena Fermentacion'
    elif resp == 1:
        respapi = 'Mediana Fermentacion'
    elif resp == 2:
        respapi = 'Moho'
    elif resp == 3:
        respapi = 'Violeta'
    return jsonify({"Recognized fermented cocoa beans:": "%s" % respapi})

@app.route('/', methods = ['GET', 'POST'])
def welcome():
    return "CONECTADO A LA API FLASK DE PYTHON"


@app.route('/process', methods = ['POST'])
def process():
    datajson = request.get_json(force=True)
    base64x = datajson['base64']

    imagePath = 'img/test.jpeg'
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(base64x, "utf-8"))))
    img.save(imagePath, 'jpeg')
    resp = predict2(imagePath) 
    respapi = ''
    if resp == 0:
        respapi = 'Buena Fermentacion'
    elif resp == 1:
        respapi = 'Mediana Fermentacion'
    elif resp == 2:
        respapi = 'Moho'
    elif resp == 3:
        respapi = 'Violeta'

    return respapi

app.run(host="0.0.0.0", port=5000, debug=True)
