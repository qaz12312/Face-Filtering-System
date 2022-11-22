import os

def folder_exist(path):
    '''
    若資料夾不存在，就創建
    '''
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'The new directory {path} is created!')