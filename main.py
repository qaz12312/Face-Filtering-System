import sys
from PyQt5 import QtWidgets
from controller.gui import GUIController


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = GUIController()
    window.show()
    sys.exit(app.exec_())