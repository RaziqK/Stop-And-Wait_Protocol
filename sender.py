import sender_config
import packets
from UDPTrans import *
import time
from pprint import pprint
import logging

logging.basicConfig(format='%(asctime)s %(message)s', filename="Logging.log", level=logging.DEBUG)


class Sender:
    
    def __init__(self):
        self.config = sender_config
        self.seq_num = 1
        self.window = []
        self.packet_count = 0

    
    def startUDPTrans(self, port):
        self.listen = UDPTrans.createServer(port)
        #print(self.listen)
    
    def sendPacket(self, packet):
        socket = UDPTrans.createSocket()
        UDPTrans.sendPacket(socket, packet, self.config.net_address,self.config.net_port)

    def retransmitPacket(self):
        for packet in self.window:
            self.sendPacket(packet)
            

    def sendSOT(self):
        packet = self.createPacket(1)
        #print(pprint(vars(packet)))
        print("Start of Transmission Packet Sent.")
        logging.info("Start of Transmission Packet Sent.")

        self.sendPacket(packet)
        receiver_response = UDPTrans.getPacket(self.listen)

        if receiver_response.getPacketType() == 1:
            print('SOT Received from server')
            logging.info("SOT Received from server")
    
    def sendEOT(self):
        packet = self.createPacket(4)
        self.sendPacket(packet)
        print("EOT Sent")
        logging.info("EOT Sent")

    def createPacket(self, packet_type):
        packet = packets.PacketCreate.createPacket(packet_type, self.seq_num,
        self.config.win_size, self.seq_num, self.config.receiver_address,       
        self.config.receiver_port, self.config.sender_address, self.config.sender_port)
        #print(packet)
        return packet

    def setConfig(self, net_address, net_port, 
    sender_address, sender_port, 
    receiver_address, receiver_port,
    max_packets, win_size, timeout):
        self.config.net_address = net_address
        self.config.net_port = net_port
        self.config.sender_address = sender_address
        self.config.sender_port = sender_port
        self.config.receiver_address = receiver_address
        self.config.receiver_port = receiver_port
        self.config.max_packets = max_packets
        self.config.win_size = win_size
        self.config.timeout = timeout

    def createWindow(self):
        for i in range(0, self.config.win_size):
            if self.packet_count < self.config.max_packets:
                
                #print(i)
                packet = self.createPacket(2)
                self.window.append(packet)
                
                #print('Sent packets: ', self.packet_count)
                #print('Packets Left: ', (self.config.max_packets - self.packet_count))
                self.packet_count += 1
                #self.sendPacket(packet)
                #print("Packet Sent!")
                #logging.info("Packet Sent!")
                self.seq_num += 1
                #print("Sequence Number", self.seq_num)
        #print(self.window)

    def timeEnd(self):
        self.timer = False
        self.waitACK = False

    def timeoutACK(self):
        self.timeEnd()
        if len(self.window) != 0:
            self.waitACK = True
            for i in range(0, len(self.window)):
                packet = self.window[i]
                #print("This is packet",packet)

                print("Sending Packet to Receiver With Sequence Number: ",getattr(packet, "seq_num") )
                pack_string = "Sending Packet to Receiver With Sequence Number: " + str(getattr(packet, "seq_num")) 
                logging.info(pack_string)

                self.sendPacket(packet)

            print('Packets Left: ', (self.config.max_packets - self.packet_count), "\n\n")
            left_string = 'Packets Left: ' + str(int(self.config.max_packets - self.packet_count))
            logging.info(left_string)

    def setACKTime(self):
        self.timer = True
        if self.timer:
            time.sleep(10)
            self.timeoutACK()
        self.ackReceived()

    def ackReceived(self):
        try:
            self.listen.settimeout(self.config.timeout)
            while len(self.window) != 0 and self.waitACK:
                print("Waiting for Acknowledgement.")
                logging.info("Waiting for Acknowledgement.")

                packet = UDPTrans.getPacket(self.listen)
                #print(pprint(vars(packet)))
                checker = packet.__dict__
                
                #print(checker)
                # print("\n\nPacket Data: ")
                # logging.info("Packet Data:")
                # for key, item in checker.items():
                #     print(key, item)
                #     x = str(key) + ": " + str(item)
                #     logging.info(x)

                if packet.getPacketType() == 3:
                    logger = "Received Acknowledgement Number: " + str(getattr(packet, "ack_num"))
                    print("Received Acknowledgement Number: ", getattr(packet, "ack_num"), "\n\n")
                    logging.info(logger)

                    self.removeWindowPacket(packet.ack_num)
        except socket.timeout:
            print('--------Ack timed out.----------')
            print("Retransmitting packet.")
            logging.info("--------Ack timed out.----------")
            logging.info("Retransmitting packet.")

            self.waitACK = False
            self.retransmitPacket()

    def removeWindowPacket(self, ack_num):
        try:
            for i in range(len(self.window)):
                if self.window[i].ack_num == ack_num:
                    self.window.pop(i)
        except IndexError:
            pass        

    def start(self):
        self.startUDPTrans(self.config.sender_port)
        self.sendSOT()
        self.window_count = 0
        print("Max Packets to Send: ", self.config.max_packets)
        max_string = "Max Packets to Send: " + str(self.config.max_packets)
        logging.info(max_string)

        while self.packet_count < self.config.max_packets:
            self.createWindow()
            self.waitACK = True
            self.setACKTime()

            while len(self.window) != 0:
                #print("loop?")
                if not self.waitACK:
                        self.setACKTime()

                
                

        self.sendEOT()
                
def main():
    try:
        print('Sender Running!')
        logging.info("Sender Running!")
        Sender().start()
    except KeyboardInterrupt:
        print('Sender ended.')
        logging.info("Sender ended.")

if __name__ == "__main__":
    main()