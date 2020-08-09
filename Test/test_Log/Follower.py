
import time 
import json
import socket
import kthread


class Follower():
    def __init__(self, src, dest):
        self.src = src # 10002
        self.dest = dest # 10001


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("",self.src))

        self.send_thread = kthread.KThread(target=self.send, args= ())
        self.recv_thread = kthread.KThread(target=self.recv, args= ())

        self.lastLogIndex = 0


    def send(self):
        while True:
            data = {'type':'HeartbeatResponse', 'state': 'alive'}

            print("\n<Heartbeat Response>: update log for {} times and still alive. / {} /".format(self.lastLogIndex, time.asctime()))

            data = json.dumps(data).encode('utf-8')

            self.sock.sendto(data, ("", self.dest))

            time.sleep(2)  

    def recv(self):
        while True:

            data, addr = self.sock.recvfrom(1024)

            data = json.loads(data)

            self.lastLogIndex = data['lastLogIndex']

            #print('\n<Heartbeat>: Log[{}] committed. / {} /'.format(self.lastLogIndex, time.asctime()))



if __name__ == '__main__':
    
    selfPort = 10002
    destPort = 10001
    
    follower = Follower(selfPort, destPort)

    follower.recv_thread.start()
    follower.send_thread.start()
