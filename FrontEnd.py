
from PyQt5 import QtWidgets
from design import Ui_MainWindow
import MyWidget
import time

class frontEnd(Ui_MainWindow):
    def __init__(self, dialog,myWidget):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.pushButton_start.clicked.connect(self.Start)
        self.pushButton_stop.clicked.connect(self.Stop)
        self.tableWidget.setHorizontalHeaderLabels(["Time","Source","Dest","Protocol","Length","Info"])
        # when cell is clicked show packet details and also hex details
        self.tableWidget.cellClicked.connect(self.showPacketDetails)
        self.tableWidget.cellClicked.connect(self.showHexPacketDetails)
        # on clicking the row we get the index
        #self.tableWidget.cellClicked.connect(self.whichRow)
        #self.tableWidget.horizontalHeaderItem().setTextAlignment(QtGui.AlignHCenter)
        #On Clicking filter the filter is applied
        self.pushButton_filter.clicked.connect(self.applyFilter)
        self.pushButton_filterRemove.clicked.connect(self.removeFilters)
        #self.my_widget = MyWidget.Integration
        MyWidget.Integration.newPacketSignal.connect(self.on_packetChanged)
        self._packetsList = []
        self.filteredList = []
        #self.my_widget.setPacket(["a","b","c","d","e","f"])
        self.sniffing=0
        MyWidget.start.setPacket(self.sniffing)
        dialog.show()

    def Start(self):
        self.sniffing=1
        MyWidget.start.setPacket(self.sniffing)
        time.sleep(0.1)
    def Stop(self):
        self.sniffing = 0
        MyWidget.start.setPacket(self.sniffing)
        time.sleep(0.1)

    def on_packetChanged(self):
        #print(MyWidget.Integration.getPacket())
        list =MyWidget.Integration.getPacket()
        self.addData(MyWidget.Integration.getPacket())

        self._packetsList.append(list)
#applyFilter not tested
    def applyFilter(self):
        #filter the list with word in text editor
        word = self.textEdit_filter.toPlainText()
        if self.filteredList == []: #1st filter
            list = self._packetsList
        else :
            list = self.filteredList
            self.filteredList = []

        #get the new filtered list (better in new thread)
        #The next throws exception(cause crashe) cuz the list is not populated
        for packet in list:
            for colData in packet:
                if colData==word:
                    self.filteredList.append(packet)
        #Clear tableWidget entries and edit box
        self.textEdit_filter.clear()
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0);
        #Set new ones
        for packet in self.filteredList:
            self.addData(packet)

    def removeFilters(self):
        # Should remove all filters and go back to initial list
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0);
        # The next throws exception(cause crashe) cuz the list is not populated
        for packet in self._packetsList:
            self.addData(packet)

# Remove Filter not tested
    '''def removeFilters(self):
    #Should remove all filters and go back to initial list
        self.tableWidget.clearContents()

        self.filteredList = []
    # The next throws exception(cause crashe) cuz the list is not populated
        for packet in self._packetsList:
            self.addData(packet)'''




    '''
    def whichRow (self,row):
        print("we are in the " + str (self.tableWidget.currentRow())+" "+ "row" )
        currentRowIndex = self.tableWidget.currentRow()
    '''
    def showPacketDetails(self):
        # we can change this 5 later to the index that will hold the packet data taken from the backend

        self.textEdit_data.setText(str(self._packetsList[self.tableWidget.currentRow()][6]))
        #print(str(self._packetsList[0]))
        #self.textEdit_data.setText(str(MyWidget.Integration.getPacket()[5]))

    def showHexPacketDetails(self):
        # we can change this 5 later to the index that will hold the packet hex data taken from the backend
        self.textEdit_hex.setText(str(self._packetsList[self.tableWidget.currentRow()][7]))
        #self.textEdit_hex.setText(str(MyWidget.Integration.getPacket()[5]))
        #print(str(self._packetsList[self.tableWidget.currentRow()][6]))

    def addData(self,list):
        #Create a empty row at bottom of table
        numRows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(numRows)
        #Add text to the row
        for i in range(6):
            self.tableWidget.setItem(numRows, i, QtWidgets.QTableWidgetItem(str(list[i])))


