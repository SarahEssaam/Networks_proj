from FrontEnd import frontEnd
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from MyWidget import myWidget

class Main(QThread):
    def __init(self):
        QThread.__init__(self)

    def run(self,myWidget):
        app = QtWidgets.QApplication(sys.argv)
        dialog = QtWidgets.QMainWindow()
        self.test_1 = frontEnd(dialog,myWidget)
        dialog.show()
        sys.exit(app.exec_())

if __name__ == '__main__':

    #Integration= myWidget()
    #M = Main()
    #M.run(Integration)
    # Sniffer().run(MyWidget)
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    test_1 = frontEnd(dialog, myWidget())
    dialog.show()
    sys.exit(app.exec_())
