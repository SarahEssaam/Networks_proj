from FrontEnd import frontEnd
import sys
from PyQt5 import QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    test_1 = frontEnd(dialog)
    dialog.show()
    sys.exit(app.exec_())