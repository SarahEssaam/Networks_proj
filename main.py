from FrontEnd import frontEnd , MyWidget
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread


class Main(QThread):
    def __init(self):
        QThread.__init__(self)

    def run(self):
        app = QtWidgets.QApplication(sys.argv)
        dialog = QtWidgets.QMainWindow()
        self.test_1 = frontEnd(dialog)
        dialog.show()
        sys.exit(app.exec_())

if __name__ == '__main__':

    Integration= MyWidget()
    M = Main()
    M.run()
    #Sniffer().run(MyWidget)
