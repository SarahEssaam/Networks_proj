from Sniffer2 import Sniffer
from FrontEnd import frontEnd
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
import time
import MyWidget


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    test_1 = frontEnd(dialog, MyWidget.Integration)
    s = Sniffer()

    s.start()


    sys.exit(app.exec_())

