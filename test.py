import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from design1 import Ui_MainWindow

class MyWidget(QObject):
    newPacketSignal = pyqtSignal()
    def __init__(self):
        # Initialize the PunchingBag as a QObject
        QObject.__init__(self)

    def setPacket(self, packet):
        self._packet = packet
        self.newPacketSignal.emit()
    def getPacket(self):
        return self._packet

class TestApp(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.pushButton_start.clicked.connect(self.Start)
        self.pushButton_stop.clicked.connect(self.Start)
        self.tableWidget.setHorizontalHeaderLabels(["Time","Source","Dest","Protocol","Length","Info"])
        #self.tableWidget.horizontalHeaderItem().setTextAlignment(QtGui.AlignHCenter)
        self.my_widget = MyWidget()
        self.my_widget.newPacketSignal.connect(self.on_packetChanged)
        # This will cause the colorChanged signal to be emitted, calling on_colorChanged
        self.my_widget.setPacket(["a","b","c","d","e","f"])
        #self.my_widget.setPacket(11)

    def Start(self):
        flagStart = True
    def Stop(self):
        flagStart = False

    def on_packetChanged(self):
        self.addData(self.my_widget.getPacket())

    def addData(self,list):
        #Create a empty row at bottom of table
        numRows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(numRows)
        #Add text to the row

        for i in range(6):
            self.tableWidget.setItem(numRows, i, QtWidgets.QTableWidgetItem(list[i]))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    test_1 = TestApp(dialog)
    dialog.show()
    sys.exit(app.exec_())