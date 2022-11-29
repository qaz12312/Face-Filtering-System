from deepface import DeepFace
import cv2
import numpy as np
import pandas as pd

# remember to modify here!
test_img = 'image we want to test'
df = DeepFace.find(img_path=test_img, db_path='db', enforce_detection=False)

df = df.sort_values(by=['VGG-Face_cosine'], ascending=False) # sort the values from the highest similarity to the lowest
df = df.reset_index(drop=True)

show = 10 # how many images to show

for i in range(show):
    tmp = cv2.imread(df.iloc[i]['identity'])
    tmp = cv2.resize(tmp, (test_img.shape[0], test_img.shape[0]), interpolation=cv2.INTER_AREA)
    hori = np.concatenate((test_img, tmp), axis=1)
    cv2.imshow('compare', hori)
    cv2.waitKey(0)
    cv2.destroyAllWindows()