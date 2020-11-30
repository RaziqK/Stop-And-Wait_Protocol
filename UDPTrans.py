import socket
import pickle
import datetime
from packets import Packet

class UDPTrans:

    def createSocket():
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def createServer(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', port))
        return s

    def getPacket(socket):
        s_data = socket.recv(1024)
        packet = pickle.loads(s_data)
        return packet

    def sendPacket(socket, packet,address=None ,port=None):
        if address != None:
            packet_dump = pickle.dumps(packet)
            socket.sendto(packet_dump, (address,port))
        else:
            packet_dump = pickle.dumps(packet)
            socket.sendto(packet_dump, (packet.getDestAddress(), packet.getDestPort()))