import random
import socket
import time
import pickle
import network_config
from UDPTrans import *
from pprint import pprint
import logging

logging.basicConfig(format='%(asctime)s %(message)s', filename="Network.log", level=logging.DEBUG)


class Network:
    def __init__(self):
        self.config = network_config
    
    def start(self):
        networkStart = True

        packets_sent = 0
        packets_dropped = 0
        packets_total = 0

        s = UDPTrans.createServer(self.config.net_port)
        print('Server is Running!')
        logging.info("Server is Running!")
        try:
            while networkStart:
                packet = UDPTrans.getPacket(s)
                #print("Packets",pprint(vars(packet)))
                checker = packet.__dict__
                #print(checker)
                # print("\n\n Packet Data: ")
                # logging.info("Packet Data:")
                # for key, item in checker.items():
                #     print(key, item)
                #     x = str(key) + ": " + str(item)
                #     logging.info(x)
                print("Packet Retrieved!")
                logging.info("Packet Retrieved!")

                print("Source Address: ", getattr(packet, "src_address"))
                src_string = "Source Address: " + str(getattr(packet, "src_address"))
                logging.info(src_string)

                print("Destination Address: ", getattr(packet, "dest_address"))
                dst_string = "Destination Address: " + str(getattr(packet, "dest_address"))
                logging.info(dst_string)

                print("Sequence Number: ", getattr(packet, "seq_num"))
                seq_string = "Sequence Number: " + str(getattr(packet, "seq_num"))
                logging.info(seq_string)
                packets_total += 1
                
                print('Total packets: ', + packets_total, '\n\n')
                total_packet_string = 'Total Packets: ' + str(packets_total), 
                logging.info(total_packet_string)

                if packet.getPacketType() == 1 or packet.getPacketType() == 4:                    
                    UDPTrans.sendPacket(s, packet, packet.getDestAddress(),
                                            packet.getDestPort())
                    packets_sent += 1

                else:
                    test = self.getDropRates()
                    if test <= self.config.drop_rate:
                        #print("Testing here",test)
                        packets_dropped += 1
                        print('----------Packet for Sequence Number ', getattr(packet,"seq_num"), ' Dropped!------------\n\n')
                        lost_str = '----------Packet for Sequence Number ' + str(getattr(packet,"seq_num")) + ' Dropped!------------'
                        logging.info(lost_str)
                    else:
                        time.sleep(self.config.average_length)
                        UDPTrans.sendPacket(s, packet)
                        packets_sent += 1

        except KeyboardInterrupt:
            print('Server Closed.')

    def getDropRates(self):
        randDropRate = random.randint(0,101)
        return randDropRate

    

def main():
    try:
        print('Network Running!')
        logging.info("Network Running!")
        Network().start()
    except KeyboardInterrupt:
        print('Receiver ended.')

if __name__ == "__main__":
    main()