import numpy as np
import os
from scipy import  misc
from keras.models import model_from_json
import pickle
import cv2
import numpy
import matplotlib.pyplot as plt
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from tensorflow.keras.optimizers import SGD
from keras.optimizers import gradient_descent_v2 
from keras.layers import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from werkzeug.utils import secure_filename

basepath = os.path.dirname(__file__)  


# Loading int2word dict
sfn = os.path.join(basepath, 'static\\model',secure_filename("int_to_word_out.pickle"))
classifier_f = open(sfn, "rb")
int_to_word_out = pickle.load(classifier_f)
classifier_f.close()

def load_model():
    
    # load json and create model
    json = os.path.join(basepath, 'static\\model',secure_filename("vein.json"))
    mdl = os.path.join(basepath, 'static\\model',secure_filename("vein.h5"))
    json_file = open(json, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model

    loaded_model.load_weights(mdl)
    print("Loaded model from disk")
    return loaded_model

def pre_process(image):
    
    image = image.astype('float32')
    image = image / 255.0
    return image
def one_hot_encode(y):

    # one hot encode outputs
    y = np_utils.to_categorical(y)
    num_classes = y.shape[1]
    return y,num_classes


def load_image(pic):
    data=[]
    fil_path = os.path.join(basepath, 'static\\login', secure_filename(pic))  
    img = cv2.imread(fil_path)    
    image = cv2.resize(img, (64, 64))
    #image=np.array(misc.imread("images/"+img))
    #image = misc.imresize(image, (64, 64))
    image=np.array([image])
    image=pre_process(image)
    model=load_model()
    prediction=model.predict(image)
    rate=np.max(prediction)
    #print(rate)
    val=int_to_word_out[np.argmax(prediction)]
    data.append(rate)
    data.append(val)
    #print(data[0])
    #print(data[1])
    return data