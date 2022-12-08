from services.face_obtain import face_obtain


class FaceController(object):
    def __init__(self):
        pass

    def extract_face(self, img_path:str)->tuple:
        is_success, msg = face_obtain(img_path)
        return is_success, msg

    def find_similar_faces(self, sex:int, count:int, img_path:list)->list:
        """
        查找相似的目標
        """
        print(f'[FaceController] Get: sex={sex}, count={count}, img_paths={img_path}')
        return []

    def find_specified_type_faces(self, sex:int, count:int)->list:
        """
        查找指定類型的面部
        """
        print(f'[FaceController] Get: sex={sex}, count={count}')
        return []

    def __repr__(self):
        return f'FaceController()'


    def __str__(self):
        return f'FaceController()'