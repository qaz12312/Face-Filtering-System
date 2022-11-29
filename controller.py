import cv2
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from ui import Ui_MainWindow


class Controller(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Controller, self).__init__()
        self.setupUi(self)
        self.bind_click_events()
        self.target_img_path = None

    
    def bind_click_events(self) -> None:
        self.pushBtn_loadImg.clicked.connect(self.click_load_image)
        self.commandLinkButton_send.clicked.connect(self.click_send)
        self.commandLinkButton_export.clicked.connect(self.click_export)

    
    def click_load_image(self) -> None:
        self.target_img_path, filter_type = QtWidgets.QFileDialog.getOpenFileName()
        print(f'load image: \n\timg_path={self.target_img_path}\n\tfilter_type={filter_type}')
        target_img = cv2.imread(self.target_img_path, -1)
        height, width, channel = target_img.shape
        bytes_per_line = 3 * width
        self.label_showImg.setPixmap(QPixmap.fromImage(QImage(target_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()))


    def click_send(self) -> None:
        radio_btns = [self.radioBtn_woman, self.radioBtn_man, self.radioBtn_all]
        for b in radio_btns:
            if b.isChecked():
                select_sex = b.text()
                break
        select_count = int(self.select_resultCount.currentText())
        print(f'infomation:\n\tselect_sex={select_sex}\n\tselect_count={select_count}\n\timg_source={self.target_img_path}')
        print('press send')


    def click_export(self) -> None:
        print('press export')

    
    def __repr__(self):
        return f'Controller()'


    def __str__(self):
        return f'Controller()'