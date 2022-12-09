import os
import datetime
import pandas as pd
import random
from faker import Faker
from styleframe import StyleFrame
import openpyxl
import os

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
        print(f"Unexpected {err}, {type(err)}")
        return False

    
def get_timestamp()->int:
    return int(datetime.datetime.today().timestamp())


def export_to_csv(file_name:str, results:list)->tuple:
    """
    [{'path': 'storages/datasets/1670184192_2.png', 'analyze': (age, gender, race)} , ...
    """
    try:
        file = f'{file_name}.xlsx'
        total_row = len(results)
        df = pd.DataFrame(columns=["人選", "姓名", "性別", "年齡", "種族", "身高", "體重"])
        fake = Faker(['it_IT', 'en_US', 'ja_JP','zh_TW'])
        names = [fake.unique.name() for i in range(total_row)]
        for i in range(total_row):
            record = results[i]
            gender = record['analyze'][1]
            height = round(random.gauss(180, 5)) if gender =='Man' else round(random.gauss(170, 5))
            # 值放到相對應的 column
            s = pd.Series([names[i], gender, record['analyze'][0], record['analyze'][2], height, random.randint(38, 80)],
                        index=["姓名", "性別", "年齡", "種族", "身高", "體重"])
            # 因為 Series 沒有橫列的標籤, 所以加進去的時候要 ignore_index=True
            df = df.append(s, ignore_index=True)
        """
        進行樣式設置
        """
        sf = StyleFrame(df) 
        #設定欄寬
        sf.set_column_width_dict(col_width_dict={
            ("人選"): 25.5,
            ("姓名", "性別", "年齡", "種族", "身高", "體重") : 20,
        }) 
        #設定列高
        all_rows = sf.row_indexes
        sf.set_row_height_dict(row_height_dict={
            all_rows[1:]: 120
        })
        #存成excel檔
        sf.to_excel(file,
                    sheet_name=file_name,
                    right_to_left=False, 
                    columns_and_rows_to_freeze='A1', 
                    row_to_add_filters=0).save() 
        """
        匯入圖片
        """
        wb = openpyxl.load_workbook(file) # 使用 load_workbook 讀取 xlsx
        ws = wb.worksheets[0] # 取得第一個工作表

        current_row = 2
        for result in results:
            fn = result['path']
            img = openpyxl.drawing.image.Image(fn) # create image instances
            ws.add_image(img, f'A{current_row}')  # 設定 sheet 工作表 An 儲存格內容
            current_row = current_row + 1
        wb.save(file) # 儲存檔案
    except Exception as err:
        return False, f"Unexpected {err}, {type(err)}"
    return True, ''