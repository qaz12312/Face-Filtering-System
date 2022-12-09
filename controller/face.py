from services.face_obtain import face_obtain
from services.face_func import *
import config.temp_variables as tv

class FaceController(object):
    def __init__(self):
        pass

    def extract_face(self, img_path:str)->tuple:
        is_success, msg = face_obtain(img_path)
        return is_success, msg

    def change_path(self, img_path:str):
        return tv.PROJECT_PATH + 'storages/faces/' + img_path
    
    def find_similar_faces(self, sex:int, count:int, img_path:list)->list:
        """
        查找相似的目標
        """
        faces = []

        if sex == 0: # woman
            db_path = tv.WOMAN_DB          
        elif sex == 1: # man
            db_path = tv.MAN_DB
        else: # both
            db_path = tv.BOTH_DB

        similar_faces = face_compare(img_path[0], db_path, count)
        similar_faces = similar_faces.apply(self.change_path)
        
        for s in similar_faces:
            print(s)
            analyze = face_analyze(s)
            faces.append(analyze)
        
        return faces

    def find_specified_type_faces(self, sex:int, face:int, eyebrow:int, eye:int, nose:int, mouth:int, count:int)->list:
        """
        查找指定類型的面部
        """
        if sex == 0: # woman
            db_path = tv.WOMAN_DB          
        elif sex == 1: # man
            db_path = tv.MAN_DB
        else: # both
            db_path = tv.BOTH_DB

        path_list = feature_detection([eye, nose, mouth], db_path, count)
        faces = []

        for p in path_list:
            path = tv.PROJECT_PATH + p
            analyze = face_analyze(path)
            faces.append(analyze)

        return faces

    def __repr__(self):
        return f'FaceController()'


    def __str__(self):
        return f'FaceController()'