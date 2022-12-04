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
        self.bind_click_events()
        self.select_sex = None
        self.select_count = None
        self.target_img_path = None
        self.face_detector = FaceController()

    def bind_click_events(self) -> None:
        self.radioBtn_woman.clicked.connect(self.click_checked)
        self.radioBtn_man.clicked.connect(self.click_checked)
        self.radioBtn_all.clicked.connect(self.click_checked)
        self.pushBtn_loadImg.clicked.connect(self.click_load_image)
        self.commandLinkButton_send.clicked.connect(self.click_send)
        self.commandLinkButton_export.clicked.connect(self.click_export)
    
    def click_checked(self) -> None:
        btn_name = self.sender().objectName()
        sex = None
        if btn_name == 'radioBtn_woman' and self.radioBtn_woman.isChecked():
            sex = 0
        elif btn_name == 'radioBtn_man' and self.radioBtn_man.isChecked():
            sex = 1
        elif btn_name == 'radioBtn_all' and self.radioBtn_all.isChecked():
            sex = 2
        else:
            return
        self.select_sex = sex
        print(f'click {self.sender().text()} / {self.select_sex}')
    
    def click_load_image(self) -> None:
        img_path, filter_type = QtWidgets.QFileDialog.getOpenFileName(self, "選擇目標圖像",os.getcwd(),"Image Files (*.png *.xpm *.jpg)")
        if len(img_path) == 0 :
            QtWidgets.QMessageBox.about(self, "注意!", "您尚未選擇目標圖像")
        else:
            self.target_img_path = img_path
            print(f'load image: \n\timg_path={self.target_img_path}\n\tfilter_type={filter_type}')
            target_img = cv2.imread(self.target_img_path)
            height, width, channel = target_img.shape
            bytes_per_line = 3 * width
            self.label_showImg.setPixmap(QPixmap.fromImage(QImage(target_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()))

    def click_send(self) -> None:
        # sex
        if self.select_sex is None :
            QtWidgets.QMessageBox.about(self, "尚未選擇性別", "請先選擇目標性別，再執行此動作")
            return
        # img
        if self.target_img_path is None :
            QtWidgets.QMessageBox.about(self, "尚未載入圖片", "請先載入目標圖像，再執行此動作")
            return
        # img success
        isSuccess, msg = self.face_detector.extract_face(self.target_img_path)
        if isSuccess:
            self.select_count = int(self.select_resultCount.currentText())
            print(f'Send infomation:\n\tselect_sex={self.select_sex}\n\tselect_count={self.select_count}\n\timg_source={self.target_img_path}')
            results = self.face_detector.find_similar_face(self.select_sex, self.select_count, msg)
        else:
            QtWidgets.QMessageBox.about(self, "請載入其他圖片", msg)


    def click_export(self) -> None:
        # 可以匯成檔案
        print('press export')

    
    def __repr__(self):
        return f'GUIController({self.select_sex},{self.target_img_path}, {self.select_count})'


    def __str__(self):
        return f'GUIController(sex={self.select_sex},img_path={self.target_img_path}, count={self.select_count})'