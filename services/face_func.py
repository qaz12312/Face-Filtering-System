from deepface import DeepFace
import pandas as pd
import cv2
import dlib
import glob
import math

def face_compare(img_path, db_path, show):
    '''
    img_path: imput image
    db_path: database we want to compare with input image
    show: how many similar images we want to show

    return: list of paths of similar images
    '''

    df = DeepFace.find(img_path=img_path, db_path=db_path, enforce_detection=False)
    df = df.sort_values(by=['VGG-Face_cosine'], ascending=False) # sort the values from the highest similarity to the lowest
    df = df.reset_index(drop=True)

    return df[:show]['identity']

def face_analyze(img_path):
    '''
    img_path: imput image

    return: dictionary, including image path and tuple of age, gender and race
    '''

    try:
        ana = DeepFace.analyze(img_path=img_path, actions=['age', 'gender', 'race'], enforce_detection=False)
        t = tuple((ana['age'], ana['gender'], max(ana['race'], key=ana['race'].get)))
        face = {'path': img_path, 'analyze': t}
    except ValueError:
        face = {}

    return face

def feature_detection(size, db_path, show):
    '''
    size: list of big (0), small (1), or both (2) (1st: eyes, 2nd: nose, 3rd: lips)
    db_path: database we want to detect
    show: how many images we want to show

    return: list of image paths
    '''

    path = glob.glob(db_path+r'*.jpg')
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("/home/hedy881028/pattern_rec/services/shape_predictor_68_face_landmarks.dat")
    cnt = 0
    path_list = []

    for p in path:
        img = cv2.imread(p)
        img = cv2.resize(img, (300, 300))
        gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        eyes = False
        nose = False
        lips = False

        for face in faces:
            landmarks = predictor(image=gray, box=face)

            # eyes
            x1 = landmarks.part(41).x
            y1 = landmarks.part(41).y
            x2 = landmarks.part(37).x
            y2 = landmarks.part(37).y
            dist = math.sqrt(pow(x1-x2, 2)+pow(y1-y2, 2))
            
            if size[0] == 0 and dist >= 6.55787101128489:
                eyes = True
            elif size[0] == 1 and dist < 6.55787101128489:
                eyes = True
            elif size[0] == 2:
                eyes = True

            # nose
            x1 = landmarks.part(31).x
            y1 = landmarks.part(31).y
            x2 = landmarks.part(35).x
            y2 = landmarks.part(35).y
            dist = math.sqrt(pow(x1-x2, 2)+pow(y1-y2, 2))
            
            if size[0] == 0 and dist >= 26.780501027381277:
                nose = True
            elif size[0] == 1 and dist < 26.780501027381277:
                nose = True
            elif size[0] == 2:
                nose = True

            # lips
            x1 = landmarks.part(66).x
            y1 = landmarks.part(66).y
            x2 = landmarks.part(57).x
            y2 = landmarks.part(57).y
            dist = math.sqrt(pow(x1-x2, 2)+pow(y1-y2, 2))
            
            if size[0] == 0 and dist >= 8.456254699988639:
                lips = True
            elif size[0] == 1 and dist < 8.456254699988639:
                lips = True
            elif size[0] == 2:
                lips = True

        if eyes == True and nose == True and lips == True:
            path_list.append(p)
            cnt += 1    

        if cnt == show:
            break

    return path_list