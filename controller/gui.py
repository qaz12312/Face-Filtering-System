import cv2
import os
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QCoreApplication, QSize, QRect
from services.ui import Ui_MainWindow
from services.utils import export_to_csv
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
        self.face = None # 圓:0, 橢圓:1, 方:2, 不拘:3
        self.eyebrow = None # 粗:0, 細:1, , 不拘:2
        self.eye = None # 圓眼:0, 長眼:1, , 不拘:2
        self.nose = None # 長:0, 短:1, , 不拘:2
        self.mouth = None # 厚:0, 薄:1, , 不拘:2
        self.face_detector = FaceController()
        # result
        self.current_result = [None, None] # for [similarity, facial]

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
        # face
        self.radioBtn_round.clicked.connect(self.click_face_checked)
        self.radioBtn_oval.clicked.connect(self.click_face_checked)
        self.radioBtn_square.clicked.connect(self.click_face_checked)
        self.radioBtn_all_face.clicked.connect(self.click_face_checked)
        # eyebrow
        self.radioBtn_fat.clicked.connect(self.click_eyebrow_checked)
        self.radioBtn_slim.clicked.connect(self.click_eyebrow_checked)
        self.radioBtn_all_eyebrow.clicked.connect(self.click_eyebrow_checked)
        # eye
        self.radioBtn_big.clicked.connect(self.click_eye_checked)
        self.radioBtn_small.clicked.connect(self.click_eye_checked)
        self.radioBtn_all_eye.clicked.connect(self.click_eye_checked)
        # nose
        self.radioBtn_long.clicked.connect(self.click_nose_checked)
        self.radioBtn_short.clicked.connect(self.click_nose_checked)
        self.radioBtn_all_nose.clicked.connect(self.click_nose_checked)
        # mouth
        self.radioBtn_thick.clicked.connect(self.click_mouth_checked)
        self.radioBtn_thin.clicked.connect(self.click_mouth_checked)
        self.radioBtn_all_mouth.clicked.connect(self.click_mouth_checked)

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
    
    def click_face_checked(self) -> None:
        """
        讀取選擇的臉型
        """
        btn_name = self.sender().objectName()
        face = None
        if btn_name == 'radioBtn_round' and self.radioBtn_round.isChecked():
            face = 0
        elif btn_name == 'radioBtn_oval' and self.radioBtn_oval.isChecked():
            face = 1
        elif btn_name == 'radioBtn_square' and self.radioBtn_square.isChecked():
            face = 2
        elif btn_name == 'radioBtn_all_face' and self.radioBtn_all_face.isChecked():
            face = 3
        else:
            return
        self.face = face
        print(f'click {self.sender().text()} / {self.face}')

    def click_eyebrow_checked(self) -> None:
        """
        讀取選擇的眉毛
        """
        btn_name = self.sender().objectName()
        eyebrow = None
        if btn_name == 'radioBtn_fat' and self.radioBtn_fat.isChecked():
            eyebrow = 0
        elif btn_name == 'radioBtn_slim' and self.radioBtn_slim.isChecked():
            eyebrow = 1
        elif btn_name == 'radioBtn_all_eyebrow' and self.radioBtn_all_eyebrow.isChecked():
            eyebrow = 2
        else:
            return
        self.eyebrow = eyebrow
        print(f'click {self.sender().text()} / {self.eyebrow}')

    def click_eye_checked(self) -> None:
        """
        讀取選擇的眼睛
        """
        btn_name = self.sender().objectName()
        eye = None
        if btn_name == 'radioBtn_big' and self.radioBtn_big.isChecked():
            eye = 0
        elif btn_name == 'radioBtn_small' and self.radioBtn_small.isChecked():
            eye = 1
        elif btn_name == 'radioBtn_all_eye' and self.radioBtn_all_eye.isChecked():
            eye = 2
        else:
            return
        self.eye = eye
        print(f'click {self.sender().text()} / {self.eye}')

    def click_nose_checked(self) -> None:
        """
        讀取選擇的鼻子
        """
        btn_name = self.sender().objectName()
        nose = None
        if btn_name == 'radioBtn_long' and self.radioBtn_long.isChecked():
            nose = 0
        elif btn_name == 'radioBtn_short' and self.radioBtn_short.isChecked():
            nose = 1
        elif btn_name == 'radioBtn_all_nose' and self.radioBtn_all_nose.isChecked():
            nose = 2
        else:
            return
        self.nose = nose
        print(f'click {self.sender().text()} / {self.nose}')

    def click_mouth_checked(self) -> None:
        """
        讀取選擇的嘴巴
        """
        btn_name = self.sender().objectName()
        mouth = None
        if btn_name == 'radioBtn_thick' and self.radioBtn_thick.isChecked():
            mouth = 0
        elif btn_name == 'radioBtn_thin' and self.radioBtn_thin.isChecked():
            mouth = 1
        elif btn_name == 'radioBtn_all_mouth' and self.radioBtn_all_mouth.isChecked():
            mouth = 2
        else:
            return
        self.mouth = mouth
        print(f'click {self.sender().text()} / {self.mouth}')

    def _img_to_QPixmap(self, img_path:str) -> None:
        img = cv2.imread(img_path)
        img = cv2.resize(img,(150, 150))
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        return QPixmap.fromImage(QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped())
    
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
            self.label_show_img.setPixmap(self._img_to_QPixmap(self.target_img_path))

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
        if self.face is None :
            return {'errTitle': "尚未選擇臉型",'errMsg': "請先選擇目標臉型，再執行此動作"}
        if self.eyebrow is None :
            return {'errTitle': "尚未選擇眉毛",'errMsg': "請先選擇目標眉毛，再執行此動作"}
        if self.eye is None :
            return {'errTitle': "尚未選擇眼睛",'errMsg': "請先選擇目標眼睛，再執行此動作"}
        if self.nose is None :
            return {'errTitle': "尚未選擇鼻子",'errMsg': "請先選擇目標鼻子，再執行此動作"}
        if self.mouth is None :
            return {'errTitle': "尚未選擇嘴巴",'errMsg': "請先選擇目標嘴巴，再執行此動作"}
        self.select_count[1] = int(self.select_result_count_facial.currentText())
        print(f'Send infomation:\n\tsex={self.select_sex[1]}\n\tface{self.face}\n\teyebrow{self.eyebrow}\n\teye{self.eye}\n\tnose{self.nose}\n\tmouth{self.mouth}\n\tcount={self.select_count[1]}')
        results = self.face_detector.find_specified_type_faces(self.select_sex[1], self.face, self.eyebrow, self.eye, self.nose, self.mouth, self.select_count[1])
        return results
    
    def _show_results(self, results:list) -> None:
        print('\n\nsend:', results,'\n\n')
        total = len(results)
        rows = int(total / 2 )
        if total % 2 != 0:
            rows = rows + 1
        self.scrollAreaWidgetContents_result.setMinimumSize(QSize(300, 200*rows)) # 寬、長
        for i in range(total):
            img_path = results[i]['path']
            rank = f"{results[i]['analyze']}"
            if i ==0:
                self.label_result_img.setPixmap(self._img_to_QPixmap(img_path))
                self.label_result_name.setText(rank)
            elif i == 1:
                self.label_result_img_3.setPixmap(self._img_to_QPixmap(img_path))
                self.label_result_name_3.setText(rank)
            elif i == 2:
                self.label_result_img_4.setPixmap(self._img_to_QPixmap(img_path))
                self.label_result_name_4.setText(rank)
            elif i == 3:
                self.label_result_img_5.setPixmap(self._img_to_QPixmap(img_path))
                self.label_result_name_5.setText(rank)
            elif i == 4:
                self.label_result_img_6.setPixmap(self._img_to_QPixmap(img_path))
                self.label_result_name_6.setText(rank)
            elif i == 5:
                self.label_result_img_7.setPixmap(self._img_to_QPixmap(img_path))
                self.label_result_name_7.setText(rank)
            elif i == 6:
                self.label_result_img_8.setPixmap(self._img_to_QPixmap(img_path))
                self.label_result_name_8.setText(rank)
            elif i == 7:
                self.label_result_img_9.setPixmap(self._img_to_QPixmap(img_path))
                self.label_result_name_9.setText(rank)
            elif i == 8:
                self.label_result_img_10.setPixmap(self._img_to_QPixmap(img_path))
                self.label_result_name_10.setText(rank)
            elif i == 9:
                self.label_result_img_11.setPixmap(self._img_to_QPixmap(img_path))
                self.label_result_name_11.setText(rank)

    def _show_facial_results(self, results:list) -> None:
        print('\n\nsend:', results,'\n\n')
        total = len(results)
        rows = int(total / 2 )
        if total % 2 != 0:
            rows = rows + 1
        self.scrollAreaWidgetContents_result_facial.setMinimumSize(QSize(300, 200*rows)) # 寬、長
        for i in range(total):
            img_path = results[i]['path']
            rank = f"{results[i]['analyze']}"
            if i ==0:
                self.label_facial_result_img.setPixmap(self._img_to_QPixmap(img_path))
                self.label_facial_result_name.setText(rank)
            elif i == 1:
                self.label_facial_result_img_3.setPixmap(self._img_to_QPixmap(img_path))
                self.label_facial_result_name_3.setText(rank)
            elif i == 2:
                self.label_facial_result_img_4.setPixmap(self._img_to_QPixmap(img_path))
                self.label_facial_result_name_4.setText(rank)
            elif i == 3:
                self.label_facial_result_img_5.setPixmap(self._img_to_QPixmap(img_path))
                self.label_facial_result_name_5.setText(rank)
            elif i == 4:
                self.label_facial_result_img_6.setPixmap(self._img_to_QPixmap(img_path))
                self.label_facial_result_name_6.setText(rank)
            elif i == 5:
                self.label_facial_result_img_7.setPixmap(self._img_to_QPixmap(img_path))
                self.label_facial_result_name_7.setText(rank)
            elif i == 6:
                self.label_facial_result_img_8.setPixmap(self._img_to_QPixmap(img_path))
                self.label_facial_result_name_8.setText(rank)
            elif i == 7:
                self.label_facial_result_img_9.setPixmap(self._img_to_QPixmap(img_path))
                self.label_facial_result_name_9.setText(rank)
            elif i == 8:
                self.label_facial_result_img_10.setPixmap(self._img_to_QPixmap(img_path))
                self.label_facial_result_name_10.setText(rank)
            elif i == 9:
                self.label_facial_result_img_11.setPixmap(self._img_to_QPixmap(img_path))
                self.label_facial_result_name_11.setText(rank)

    def click_send(self) -> None:
        """
        送資料去處理
        """
        btn_name = self.sender().objectName()
        if btn_name == 'commandLinkButton_send':
            results = self._send_similarity_requires()
            if isinstance(results, dict):
                QtWidgets.QMessageBox.about(self, results['errTitle'], results['errMsg'])
            elif len(results) == 0:
                QtWidgets.QMessageBox.about(self, "唉呦", "沒有找到指定的相似五官")
            else:
                self.current_result[self.current_page] = results
                self._show_results(results)
        elif btn_name == 'commandLinkButton_send_facial':
            results = self._send_facial_selection_requires()
            if isinstance(results, dict):
                QtWidgets.QMessageBox.about(self, results['errTitle'], results['errMsg'])
            elif len(results) == 0:
                QtWidgets.QMessageBox.about(self, "唉呦", "沒有找到指定的目標五官")
            else:
                self.current_result[self.current_page] = results
                self._show_facial_results(results)
        else:
            return

    def click_export(self) -> None:
        """
        可以匯成檔案
        """
        if self.current_result[self.current_page] is None :
            QtWidgets.QMessageBox.about(self, "尚未進行搜尋", "請確認要求皆已填寫，並執行送出")
            return
        btn_name = self.sender().objectName()
        file_name = None
        if btn_name == 'commandLinkButton_export':
            file_name = '人臉過濾系統_相似度結果'
        elif btn_name == 'commandLinkButton_export_facial':
            file_name = '人臉過濾系統_五官選取結果'
        ret, msg = export_to_csv(file_name, self.current_result[self.current_page])
        if ret:
            QtWidgets.QMessageBox.about(self, "匯出成功", f"已匯出成「{file_name}.csv」")
        else:
            QtWidgets.QMessageBox.about(self, "匯出失敗!", msg)
        print(f'export file name={file_name} result={ret}')
    
    def __repr__(self):
        return f'GUIController({self.select_count})'

    def __str__(self):
        return f'GUIController(count={self.select_count})'