import os
import datetime

def folder_exist(path:str)->bool:
    '''
    若資料夾不存在，就創建
    '''
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f'The new directory {path} is created!')
        return True
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return False

    
def get_timestamp()->int:
    return int(datetime.datetime.today().timestamp())