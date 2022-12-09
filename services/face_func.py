from deepface import DeepFace
import pandas as pd
import cv2
import dlib

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

    return: dictionary, tuple of age, gender and race
    '''

    try:
        ana = DeepFace.analyze(img_path=img_path, actions=['age', 'gender', 'race'], enforce_detection=False)
        t = tuple((ana['age'], ana['gender'], max(ana['race'], key=ana['race'].get)))
        face = {'path': img_path, 'analyze': t}
    except ValueError:
        face = {}

    return face

def feature_extraction(img_path):
    '''
    img_path: input image

    return: tuple of age, gender and race
    '''

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        x1 = face.left() # left point
        y1 = face.top() # top point
        x2 = face.right() # right point
        y2 = face.bottom() # bottom point

        landmarks = predictor(image=gray, box=face)

        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y

            cv2.circle(img=img, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)

    cv2.imshow(winname="Face", mat=img)
    cv2.waitKey(delay=0)
    cv2.destroyAllWindows()
