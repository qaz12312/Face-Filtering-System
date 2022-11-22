"""
source:
使用MTCNN模型來偵測人臉，用FaceNet提取臉部特徵
"""
import mtcnn
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# from IPython.display import display
import temp_variables
import utils

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


def get_model(file_name:str):
    '''
    載入model，若本地端無檔案則儲存在 temp_variables.PROJECT_PATH/facenet/file_name
    '''
    # (檔案名稱, 原始url, 緩存file位置, 存在哪個子dir下, 解壓縮檔案)
    file_locl_path = tf.keras.utils.get_file(file_name, origin=temp_variables.FACENET_URL, cache_dir=temp_variables.PROJECT_PATH, cache_subdir='facenet', extract=False)
    model = load_model(file_locl_path)
    # (Keras model instance, 結構圖存放位置, 顯示shape資訊, 顯示layer名稱, Dots per inch)
    model_arch = tf.keras.utils.plot_model(model, to_file='./facenet/model_arch.png', show_shapes=True, show_layer_names=True, dpi=64)
    # display(model_arch)  # print 結構圖
    return model


def show_detected_img(pixels:np.array, detected:list)->None:
    '''
    show 原圖 + 偵測到的結果
    pixels: 原圖
    detected: 偵測到的臉範圍、眼睛*2、鼻子、嘴巴*2
    '''
    plt.figure(figsize=(pixels.shape[1]*6//pixels.shape[0], 6)) # =( round((h/w)*6), 6 )
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
    plt.show()


def extract_face_save(pixels:np.array, detected:list)->list:
    '''
    save 偵測到的結果圖
    '''
    utils.folder_exist('./datasets')
    face_img = list()
    for i, i_result in enumerate(detected):
        plt.figure()
        x1, y1, width, height = i_result['box']
        bias_x, bias_y = width/4, height/4
        x1, y1 = round(abs(x1)-bias_x), round(abs(y1)-bias_y)
        x2, y2 = round(x1 + width + 2 * bias_x), round(y1 + height + bias_y)
        face = cv2.resize(pixels[y1:y2, x1:x2], (160, 160)).astype('float32')
        plt.imshow(face/255)
        face_img.append(face)
        plt.axis(False)
        plt.tight_layout()           
        plt.savefig(f'./datasets/{i + 1}.png')
        plt.title(f'{i_result["confidence"]:.2f}')
        plt.show()
    return face_img


def get_face_embedding(model, face_img):
    '''
    輸入一張人臉照片提取特徵，把它表示成一個d維空間的向量
    '''
    face_img = (face_img-tf.math.reduce_mean(face_img))/tf.math.reduce_std(face_img)
    embedding = model.predict(face_img[tf.newaxis,:])
    embedding = embedding/tf.norm(embedding)
    return embedding


if __name__ == '__main__':
    img_path = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTu0rkPWvi3aDNYySS7OpYDxic3qp0aIvxqQ&usqp=CAU'
    model = get_model('keras_model.h5')
    # create the mtcnn face detector
    detector = mtcnn.MTCNN()
    pixels_arr = get_img_pixels('url', img_path)
    results_list = detector.detect_faces(pixels_arr)
    show_detected_img(pixels_arr, results_list)
    face_imgs = extract_face_save(pixels_arr, results_list)
    face_embedding = list()
    for img in face_imgs:
        embedding = get_face_embedding(model, img)
        face_embedding.append(embedding)
    face_embedding = np.vstack(face_embedding)



