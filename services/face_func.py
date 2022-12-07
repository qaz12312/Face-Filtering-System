from deepface import DeepFace
import numpy as np
import pandas as pd

def face_compare(img_path, db_path, show):
    '''
    img_path: imput image
    db_path: database we want to compare with input image
    show: how many similar images we want to show

    return: paths of similar images
    '''

    df = DeepFace.find(img_path=img_path, db_path=db_path, enforce_detection=False)
    df = df.sort_values(by=['VGG-Face_cosine'], ascending=False) # sort the values from the highest similarity to the lowest
    df = df.reset_index(drop=True)

    return df[:show]['idnetity']

def face_analyze(img_path):
    '''
    img_path: imput image

    return: tuple of age, gender and race
    '''

    ana = DeepFace.analyze(img_path=img_path, actions=['age', 'gender', 'race'], enforce_detection=False)
    t = tuple(ana['age'], ana['gender'], ana['race'])

    return t

def feature_extraction():
    pass
