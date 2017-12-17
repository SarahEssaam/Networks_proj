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
        self._packetsList = []

    def setPacket(self, packet):
        self._packet = packet
        # i added the coming two lines to save incoming packets into packetlist
        self._packetsList.append(self._packet)
        self.newPacketSignal.emit()

    def getPacket(self):
        return self._packet

    def getPacketList(self):
        return self._packetsList

class frontEnd(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.pushButton_start.clicked.connect(self.Start)
        self.pushButton_stop.clicked.connect(self.Start)
        self.tableWidget.setHorizontalHeaderLabels(["Time","Source","Dest","Protocol","Length","Info"])
        # when cell is clicked show packet details and also hex details
        self.tableWidget.cellClicked.connect(self.showPacketDetails)
        self.tableWidget.cellClicked.connect(self.showHexPacketDetails)
        # on clicking the row we get the index
        #self.tableWidget.cellClicked.connect(self.whichRow)
        #self.tableWidget.horizontalHeaderItem().setTextAlignment(QtGui.AlignHCenter)
        self.my_widget = MyWidget()
        self.my_widget.newPacketSignal.connect(self.on_packetChanged)
        # This will cause the colorChanged signal to be emitted, calling on_colorChanged
        self.my_widget.setPacket(["a","b","c","d","e","f"])

    def Start(self):
        flagStart = True
    def Stop(self):
        flagStart = False

    def on_packetChanged(self):
        self.addData(self.my_widget.getPacket())
    '''
    def whichRow (self,row):
        print("we are in the " + str (self.tableWidget.currentRow())+" "+ "row" )
        currentRowIndex = self.tableWidget.currentRow()
    '''
    def showPacketDetails(self):
        # we can change this 5 later to the index that will hold the packet data taken from the backend
         self.textEdit_data.setText(str(self.my_widget.getPacket()[self.tableWidget.currentRow()][6]))

    def showHexPacketDetails(self):
        # we can change this 5 later to the index that will hold the packet hex data taken from the backend
         self.textEdit_hex.setText(str(self.my_widget.getPacket()[self.tableWidget.currentRow()][7]))


    def addData(self,list):
        #Create a empty row at bottom of table
        numRows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(numRows)
        #Add text to the row
        for i in range(6):
            self.tableWidget.setItem(numRows, i, QtWidgets.QTableWidgetItem(list[i]))

