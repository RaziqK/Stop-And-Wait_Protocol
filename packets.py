import pickle

class Packet:
    def __init__(self):
        self.packet_type = 0
        self.seq_num = 0
        self.data = ""
        self.win_size = 0
        self.ack_num = 0
        self.dest_address = ""
        self.dest_port = ""
        self.src_address = ""
        self.src_port = ""
    
    def getPacketType(self):
        return self.packet_type

    def setPacketType(self, packet_type):
        self.packet_type = packet_type
    
    def getSeqNum(self):
        return self.seq_num
    
    def setSeqNum(self, seq_num):
        self.seq_num = seq_num

    def getData(self):
        return self.data
    
    def setData(self, data):
        self.data = data

    def getWinSize(self):
        return self.win_size

    def setWinSize(self, win_size):
        self.win_size = win_size

    def getAckNum(self):
        return self.ack_num
    
    def setAckNum(self, ack_num):
        self.ack_num = ack_num

    def getDestAddress(self):
        return self.dest_address
    
    def setDestAddress(self, dest_address):
        self.dest_address = dest_address
    
    def getDestPort(self):
        return self.dest_port
    
    def setDestPort(self, dest_port):
        self.dest_port = dest_port

    def getSrcAddress(self):
        return self.src_address
    
    def setSrcAddress(self, src_address):
        self.src_address = src_address

    def getSrcPort(self):
        return self.src_port
    
    def setSrcPort(self, src_port):
        self.src_port = src_port

class PacketCreate:
    def createPacket(packet_type, seq_num, win_size, ack_num, dest_address, dest_port, src_address, src_port):

        packet = Packet()
        if packet_type == 1:
            packet.setData('Start of Transmission')
        elif packet_type == 2:
            packet.setData('Packet Number: {0}'.format(seq_num))
        elif packet_type == 3:
            packet.setData('Acknowledgement Number: {0}'.format(ack_num))
        elif packet_type == 4:
            packet.setData('End of Transmission')

        packet.setPacketType(packet_type)
        packet.setSeqNum(seq_num)
        packet.setWinSize(win_size)
        packet.setAckNum(ack_num)
        packet.setDestAddress(dest_address)
        packet.setDestPort(dest_port)
        packet.setSrcAddress(src_address)
        packet.setSrcPort(src_port)

        return packet