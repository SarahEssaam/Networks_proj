from PyQt5.QtCore import QObject, pyqtSignal

class myWidget(QObject):
    newPacketSignal = pyqtSignal()
    #newPacketSignal= SIGNAL('add_packet(QString)')
    def __init__(self):
        # Initialize the PunchingBag as a QObject
        QObject.__init__(self)


    def setPacket(self, packet):
        self._packet = packet
        # i added the coming two lines to save incoming packets into packetlist
        self.newPacketSignal.emit()
        #self.list=packet

    def getPacket(self):
        return self._packet

Integration= myWidget()
start= myWidget()
