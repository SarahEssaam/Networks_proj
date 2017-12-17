from PyQt5.QtCore import QObject, pyqtSignal

class myWidget(QObject):
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

