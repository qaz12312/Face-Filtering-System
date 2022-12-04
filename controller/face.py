from services.face_obtain import face_obtain


class FaceController(object):
    def __init__(self):
        pass

    def extract_face(self, img_path:str)->tuple:
        isSuccess, msg = face_obtain(img_path)
        return isSuccess, msg

    def find_similar_face(self, sex:int, count:int, img_path:list):
        print(f'Get: sex={sex}, count={count}, img_paths={img_path}')
        pass

    def __repr__(self):
        return f'FaceController()'


    def __str__(self):
        return f'FaceController()'