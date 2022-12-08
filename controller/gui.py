import cv2
import os
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from services.ui import Ui_MainWindow
from controller.face import FaceController


class GUIController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(GUIController, self).__init__()
        self.setupUi(self)
        self.bind_events()
        self.current_page = 0 # similarity:0, facial:1
        self.select_sex = [None, None] # for [similarity, facial]
        self.select_count = [None, None] # for [similarity, facial]
        # for similarity
        self.target_img_path = None
        # for  facial
        self.facial = None
        self.eyebrow = None
        self.eye = None
        self.nose = None
        self.mouth = None
        self.face_detector = FaceController()

    def bind_events(self) -> None:
        self.similarity_action.triggered.connect(self.change_page)
        self.facial_selection_action.triggered.connect(self.change_page)
        # similarity page
        self.radioBtn_woman.clicked.connect(self.click_sex_checked)
        self.radioBtn_man.clicked.connect(self.click_sex_checked)
        self.radioBtn_all.clicked.connect(self.click_sex_checked)
        self.pushBtn_load_img.clicked.connect(self.click_load_target_img)
        self.commandLinkButton_send.clicked.connect(self.click_send)
        self.commandLinkButton_export.clicked.connect(self.click_export)
        # facial page
        self.radioBtn_woman_facial.clicked.connect(self.click_sex_checked)
        self.radioBtn_man_facial.clicked.connect(self.click_sex_checked)
        self.radioBtn_all_facial.clicked.connect(self.click_sex_checked)
        self.commandLinkButton_send_facial.clicked.connect(self.click_send)
        self.commandLinkButton_export_facial.clicked.connect(self.click_export)

    def change_page(self) -> None:
        menu_name = self.sender().objectName()
        go_page_idx = -1
        if menu_name == 'similarity_action':
            go_page_idx = 0
        elif menu_name == 'facial_selection_action':
            go_page_idx = 1
        else:
            return
        self.stackedWidget.setCurrentIndex(go_page_idx)
        self.current_page = go_page_idx

    def click_sex_checked(self) -> None:
        """
        讀取選擇的性別
        """
        btn_name = self.sender().objectName()
        sex = None
        if (btn_name == 'radioBtn_woman' and self.radioBtn_woman.isChecked()) or (btn_name == 'radioBtn_woman_facial' and self.radioBtn_woman_facial.isChecked()):
            sex = 0
        elif (btn_name == 'radioBtn_man' and self.radioBtn_man.isChecked()) or (btn_name == 'radioBtn_man_facial' and self.radioBtn_man_facial.isChecked()):
            sex = 1
        elif (btn_name == 'radioBtn_all' and self.radioBtn_all.isChecked()) or (btn_name == 'radioBtn_all_facial' and self.radioBtn_all_facial.isChecked()):
            sex = 2
        else:
            return
        self.select_sex[self.current_page] = sex
        print(f'click {self.sender().text()} / {self.select_sex[self.current_page]}')
    
    def click_load_target_img(self) -> None:
        """
        讀取選擇的目標圖像
        """
        img_path, filter_type = QtWidgets.QFileDialog.getOpenFileName(self, "選擇目標圖像", os.getcwd(), "Image Files (*.png *.xpm *.jpg)")
        if len(img_path) == 0 :
            QtWidgets.QMessageBox.about(self, "注意!", "您尚未選擇目標圖像")
        else:
            self.target_img_path = img_path
            print(f'load image: \n\timg_path={self.target_img_path}\n\tfilter_type={filter_type}')
            target_img = cv2.imread(self.target_img_path)
            height, width, channel = target_img.shape
            bytes_per_line = 3 * width
            self.label_show_img.setPixmap(QPixmap.fromImage(QImage(target_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()))
    
    def _send_similarity_requires(self) -> list:
        """
        傳送人臉相似度的需求
        """
        # sex
        if self.select_sex[0] is None :
            return {'errTitle': "尚未選擇性別",'errMsg': "請先選擇目標性別，再執行此動作"}
        # img
        if self.target_img_path is None :
            return {'errTitle': "尚未載入圖片",'errMsg': "請先載入目標圖像，再執行此動作"}
        # img success
        is_success, msg = self.face_detector.extract_face(self.target_img_path)
        if is_success:
            self.select_count[0] = int(self.select_result_count.currentText())
            print(f'Send infomation:\n\tselect_sex={self.select_sex[0]}\n\tselect_count={self.select_count[0]}\n\timg_source={self.target_img_path}')
            return self.face_detector.find_similar_faces(self.select_sex[0], self.select_count[0], msg)
        else:
            return {'errTitle': "請載入其他圖片",'errMsg': msg}

    def _send_facial_selection_requires(self) -> list:
        """
        傳送人臉過濾的需求
        """
        # sex
        if self.select_sex[1] is None :
            return {'errTitle': "尚未選擇性別",'errMsg': "請先選擇目標性別，再執行此動作"}
        self.select_count[1] = int(self.select_result_count_facial.currentText())
        print(f'Send infomation:\n\tselect_sex={self.select_sex[1]}\n\tselect_count={self.select_count[1]}')
        results = self.face_detector.find_specified_type_faces(self.select_sex[1], self.select_count[1])
        return results
    
    def click_send(self) -> None:
        """
        送資料去處理
        """
        btn_name = self.sender().objectName()
        print(f'{btn_name} press export')
        if btn_name == 'commandLinkButton_send':
            results = self._send_similarity_requires()
        elif btn_name == 'commandLinkButton_send_facial':
            results = self._send_facial_selection_requires()
        else:
            return
        # show result
        if isinstance(results, dict):
            QtWidgets.QMessageBox.about(self, results['errTitle'], results['errMsg'])
        elif len(results) == 0:
            QtWidgets.QMessageBox.about(self, "唉呦", "沒有找到指定的目標五官")
        else:
            pass

    def click_export(self) -> None:
        """
        可以匯成檔案
        """
        btn_name = self.sender().objectName()
        print(f'{btn_name} press export')
        # if btn_name == 'commandLinkButton_export':
        #     pass
        # elif btn_name == 'commandLinkButton_export_facial':
        #     pass
    
    def __repr__(self):
        return f'GUIController({self.select_count})'

    def __str__(self):
        return f'GUIController(count={self.select_count})'