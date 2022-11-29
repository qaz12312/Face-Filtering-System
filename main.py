import sys
from PyQt5 import QtWidgets
from controller import Controller
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Controller()
    window.show()
    sys.exit(app.exec_())