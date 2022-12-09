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
        return tv.PROJECT_PATH + '/storages/faces/' + img_path
    
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
        
        for img in img_path:
            similar_faces = face_compare(img, db_path, count)
            similar_faces = similar_faces.apply(self.change_path)
            tmp = []
            
            for s in similar_faces:
                analyze = face_analyze(s)
                tmp.append(analyze)

            faces.append(tmp)
        return faces

    def find_specified_type_faces(self, sex:int, face:int, eyebrow:int, eye:int, nose:int, mouth:int, count:int)->list:
        """
        查找指定類型的面部
        """
        print(f'\n[FaceController]\nGet: sex={sex}, face={face}, eyebrow={eyebrow}, eye={eye}, nose={nose}, mouth={mouth}, count={count}')
        return []

    def __repr__(self):
        return f'FaceController()'


    def __str__(self):
        return f'FaceController()'