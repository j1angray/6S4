
import time 
import json
import pickle
import socket
import kthread
from RPC import *
from Server import *


class Client():
    def __init__(self, id, port):
        self.id = id # 111
        self.port = port # 10000
        self.dest = None
        self.lastLogIndex = 0
        self.lastLogTerm = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("",self.port))

        self.rpc_call = kthread.KThread(target=self.rpc_process, args= ())

 
    def rpc_process(self):

        while True:
            data, addr = self.sock.recvfrom(1024)
            msg = pickle.loads(data)

            #type = msg.type
            self.dest = msg.src
            destPort = msg.port
            self.lastLogTerm = msg.term

            print("<Log Commit>: {} times by Leader[{}] in Term[{}].".format(self.lastLogIndex, msg.src, msg.term))

            self.lastLogIndex += 1

            reply = ClientEntryResponseRPC(self.id, self.dest, self.lastLogTerm, self.lastLogIndex, self.port)
            
            print('\n<Client Append Entry>: Log[{}]. / {} /'.format(self.lastLogIndex, time.asctime()))

            self.sock.sendto(pickle.dumps(reply), ("", destPort))

            time.sleep(2)


if __name__ == '__main__':
    
    client = Client(111, 10000)
    client.rpc_call.start()

