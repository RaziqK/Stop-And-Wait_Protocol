import sender_config
from sender import Sender
from packets import *
from UDPTrans import *
from pprint import pprint
import logging

logging.basicConfig(format='%(asctime)s %(message)s', filename="Logging.log", level=logging.DEBUG)


class Receiver(Sender):
    def __init__(self):
        self.seq_num = 0
        self.asked_packets = []
        self.config = sender_config

    def start(self):
        self.startUDPTrans(sender_config.receiver_port)
        self.SOTCheck()
       # print("Work?")
        self.receiver_check = True

        packets_total = 0
        dupe_ack_total = 0

        while self.receiver_check:
            packet = UDPTrans.getPacket(self.listen)
            print("Packet Received!")
            logging.info("Packet Received!")
            checker = packet.__dict__
            #print(checker)
            print("\n\n Packet Data: ")
            logging.info("Packet Data:")
            for key, item in checker.items():
                print(key, item)
                x = str(key) + ": " + str(item)
                logging.info(x)
           
            #print(pprint(vars(packet)))
            
            packet_type = packet.getPacketType()
            #print("Packet_Type  :", packet_type)

            if packet_type == 4:
                print("End of Transmission")
                print("All Packets received!")
                print("Duplicate ACKs: ", dupe_ack_total)
                dupe_ack_str = "Duplicate ACKs: " + str(dupe_ack_total)
                logging.info("End of Transmission")
                logging.info("All Packets received!")
                logging.info(dupe_ack_str)
                self.receiver_check = False
                break
            elif packet_type == 2:
                self.seq_num = packet.seq_num
                ack_packet = self.createPacket(3)
                self.sendPacket(ack_packet)
                print("Sending ACK Packet")
                logging.info("Sending ACK Packet")
                find_ACK = self.findACKPacket(packet.seq_num)
                #print("Finding aCK ",find_ACK)
                if not find_ACK:
                    packets_total += 1
                else:
                    dupe_ack_total += 1
                    print("-----Duplicate ACK Occurred!-----")
                    logging.info("-----Duplicate ACK Occurred!-----")
            self.asked_packets.append(packet)
    

    def findACKPacket(self, seq_num):
        #print(len(self.asked_packets))
        for i in range(0, len(self.asked_packets)):
            #print("Parameter: ", seq_num)
            #print("Asked Packets:", self.asked_packets[i].seq_num)
            if self.asked_packets[i].seq_num == seq_num:
                return True
        return False

    def SOTCheck(self):
        sot_packet = UDPTrans.getPacket(self.listen)

        if sot_packet.getPacketType() == 1:
            print("Received SOT from Sender")
            logging.info("Received SOT from Sender")
            packet = self.createPacket(1)
            #print(packet)
            self.sendPacket(packet)
        else:
            self.SOTWait(packet)

    def createPacket(self, packet_type):
        packet = PacketCreate.createPacket(packet_type,self.seq_num,
        sender_config.win_size,self.seq_num,sender_config.sender_address,
        sender_config.sender_port,
        sender_config.receiver_address,sender_config.receiver_port)
        return packet

def main():
    try:
        print('Receiver Running!')
        logging.info("Receiver Running!")
        Receiver().start()
    except KeyboardInterrupt:
        print('Receiver ended.')

if __name__ == "__main__":
    main()