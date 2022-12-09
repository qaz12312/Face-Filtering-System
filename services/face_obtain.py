"""
source:
使用MTCNN模型來偵測人臉
"""
import mtcnn
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import services.utils as utils
import config.temp_variables as vars

def get_img_pixels(source_type:str, path:str)->np.array:
    '''
    從 img url 轉成 pixel 的 3D Numpy array
    '''
    if source_type == 'url':
        name = path.split('/')[-1]
        filename = tf.keras.utils.get_file(name, origin=path)
    elif source_type == 'file':
        filename = path
    else:
        raise ValueError('input source_type error: only `url` or `file`')
    
    # 其他參數: https://www.twblogs.net/a/5cd53ffbbd9eee67a77f4cd8#:~:text=2%E3%80%81-,load_img(),-%E5%87%BD%E6%95%B8%E5%8E%9F%E5%9E%8B%E7%88%B2
    img_pil = tf.keras.preprocessing.image.load_img(filename) # shape=(寬, 高, channels數)
    pixels_arr = tf.keras.preprocessing.image.img_to_array(img_pil)
    # pixels_arr = np.expand_dims(pixels_arr, axis=0) # shape=(1, 寬, 高, channels數) --> 有時模型要求的輸入為(None(表batch), 寬, 高, channels數)
    return pixels_arr


def show_detected_img(pixels:np.array, detected:list)->None:
    '''
    show 原圖 + 偵測到的結果
    pixels: 原圖
    detected: 偵測到的臉範圍、眼睛*2、鼻子、嘴巴*2
    '''
    plt.figure(figsize=(pixels.shape[1]*3//pixels.shape[0], 3)) # =( round((h/w)*6), 6 )
    plt.imshow(pixels/255)
    plt.axis(False)
    ax = plt.gca()
    for i_result in detected:
        # plot 臉範圍
        x1, y1, width, height = i_result['box']
        bias_x, bias_y = width/4, height/4
        x1, y1 = abs(x1)-bias_x, abs(y1)-bias_y
        width, height = width + 2*bias_x, height + bias_y
        ax.add_patch(mpatches.Rectangle((x1, y1), width, height, ec='red', alpha=1, fill=None))
        # plot 信心值
        plt.text(x1, y1, f'{i_result["confidence"]:.2f}', color='yellow') 
        # plot 眼睛*2、鼻子、嘴巴*2
        for val in i_result['keypoints'].values():
            ax.add_patch(mpatches.Circle(val, 1, color='blue'))
    # plt.show()


def extract_face_save(pixels:np.array, detected:list)->list:
    '''
    save 偵測到的結果圖
    '''
    utils.folder_exist(vars.FACES_PATH)
    img_prefix = f'{utils.get_timestamp()}'
    img_paths = list()
    for i, i_result in enumerate(detected):
        plt.figure(figsize=(3, 3))  # 設定結果圖的圖片大小
        x1, y1, width, height = i_result['box']
        bias_x, bias_y = width/4, height/4
        x1, y1 = round(abs(x1)-bias_x), round(abs(y1)-bias_y)
        x2, y2 = round(x1 + width + 2 * bias_x), round(y1 + height + bias_y)
        face = pixels[y1:y2, x1:x2].astype('float32')
        plt.imshow(face/255)
        plt.axis(False)
        plt.tight_layout()
        img_path = f'{vars.FACES_PATH}/{img_prefix}_{i + 1}.png'       
        plt.savefig(img_path)
        img_paths.append(img_path)
        plt.title(f'{i_result["confidence"]:.2f}')
        # plt.show()
    return img_paths


def face_obtain(img_path:str) -> tuple:
    try:
        detector = mtcnn.MTCNN()
        pixels_arr = get_img_pixels('file', img_path)
        results_list = detector.detect_faces(pixels_arr)
        if len(results_list) == 0:
            raise ValueError('沒有偵測到人臉')
        show_detected_img(pixels_arr, results_list)
        img_paths = extract_face_save(pixels_arr, results_list)
        return True, img_paths
    except ValueError as e:
        msg, = e.args
        return False, msg


if __name__ == '__main__':
    try:
        img_path = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTu0rkPWvi3aDNYySS7OpYDxic3qp0aIvxqQ&usqp=CAU'
        # create the mtcnn face detector
        detector = mtcnn.MTCNN()
        pixels_arr = get_img_pixels('url', img_path)
        results_list = detector.detect_faces(pixels_arr)
        show_detected_img(pixels_arr, results_list)
        face_imgs = extract_face_save(pixels_arr, results_list)
    except ValueError as msg:
        print(msg)