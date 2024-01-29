from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
from PIL import Image
import os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import tensorflow as tf
from tensorflow.keras.preprocessing import image #type: ignore

diseaseTypeModel, pcamodel, diseaseModels = None, None, None

def loadModels():
    global diseaseTypeModel, pcamodel, diseaseModels

    diseaseTypeModel=joblib.load('Project1\\firstProj\\AIModels\\model.joblib')
    pcamodel=joblib.load('Project1\\firstProj\\AIModels\\pca_model.joblib')

    diseaseModels = [
        joblib.load('Project1\\firstProj\\AIModels\\2_svm_model.pkl'),
        tf.keras.models.load_model('Project1\\firstProj\\AIModels\\BreastCancerModel'), # type: ignore
        tf.keras.models.load_model('Project1\\firstProj\\AIModels\\chest-xray-model.h5'), # type: ignore
        tf.keras.models.load_model('Project1\\firstProj\\AIModels\\RetinalDiseaseCNN'), # type: ignore
        tf.keras.models.load_model('Project1\\firstProj\\AIModels\\SkinDiseaseModel') # type: ignore
    ]
    print("Models Loaded")

def detectDisease(fname):
    global diseaseTypeModel, pcamodel, diseaseModels

    if diseaseTypeModel is None or pcamodel is None or diseaseModels is None:
        return {'class': 'Models not loaded'}

    diseaseType = ['Dementia dataset', 'Breast Cancer dataset', 'Pneumonia dataset', 'Retinal Disease dataset', 'Skin Disease dataset']
    class_names = [
        ['Mild Demented', 'Moderate Demented', 'Non Demented', 'Very Mild Demented'],
        ['Benign', 'Malignant', 'Normal'],
        ['NORMAL', 'PNEUMONIA'],
        ['ARMD', 'DN', 'DR', 'MH', 'NORMAL', 'ODC'],
        ['Actinic keratosis', 'Atopic Dermatitis', 'Benign Keratosis', 'Dermatofibroma', 'Melanocytic nevus', 'Melanoma', 'Squamous cell carcinoma', 'Tinea Ringworm', 'Vascular lesion']
    ]

    # resolution of images on which the models are trained
    resolution=[
        (128, 128),
        (128, 128),
        (256, 256),
        (224, 224),
        (224, 224)
    ]

    # diseaseTypeModel=joblib.load('Project1\\firstProj\\AIModels\\model.joblib')
    # pcamodel=joblib.load('Project1\\firstProj\\AIModels\\pca_model.joblib')

    # diseaseModels = [
    #     joblib.load('Project1\\firstProj\\AIModels\\2_svm_model.pkl'),
    #     tf.keras.models.load_model('Project1\\firstProj\\AIModels\\BreastCancerModel'), # type: ignore
    #     tf.keras.models.load_model('Project1\\firstProj\\AIModels\\chest-xray-model.h5'), # type: ignore
    #     tf.keras.models.load_model('Project1\\firstProj\\AIModels\\RetinalDiseaseCNN'), # type: ignore
    #     tf.keras.models.load_model('Project1\\firstProj\\AIModels\\SkinDiseaseModel') # type: ignore
    # ]

    img = Image.open("Project1\\firstProj\\uploads\\"+fname)

    # print(type(img), "jfiegfipeughpiwughpwtghTGHWTUIHWTUIHRTUHTRHUHYITHYIT")

    g_img = img.convert('L')    
    g_img = g_img.resize((64, 64)) # 64 is the size we trained the model on
    img_array = np.array(g_img).flatten()

    img_array=np.expand_dims(img_array, axis=0)

    img_pca=pcamodel.transform(img_array)
    predicted_label=diseaseTypeModel.predict(img_pca)[0]

    print(predicted_label, type(predicted_label))
    _img = image.load_img("Project1\\firstProj\\uploads\\"+fname, target_size=resolution[predicted_label])

    if predicted_label==0: # flattenning the image since the Dimentia is trained on ML model and not on CNN model
        _img = np.array(_img)
        _img = _img.flatten()

    _img_array = np.expand_dims(_img, axis=0)
    pld=diseaseModels[predicted_label].predict(_img_array)
    label = np.argmax(pld)

    return {'class': class_names[predicted_label][label]}