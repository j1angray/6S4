
import time 
import json
import socket
import kthread


class Client():
    def __init__(self, src, dest):
        self.src = src # 10000
        self.dest = dest # 10001
        self.index = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("",self.src))

        self.send_thread = kthread.KThread(target=self.send, args= ())
        self.recv_thread = kthread.KThread(target=self.recv, args= ())


    def send(self):

        while True:
            data = {'type': 'ClientAppendEntry', 'index': self.index}

            print('\n<Client Append Entry>: Log[{}]. / {} /'.format(self.index, time.asctime()))

            data = json.dumps(data).encode('utf-8')

            self.sock.sendto(data, ("", self.dest))

            time.sleep(5)  


    def recv(self):

        while True:
            data, addr = self.sock.recvfrom(1024)

            data = json.loads(data)
            print("<Log Commit>: {}.".format(data['success']))

            self.index +=1


if __name__ == '__main__':

    addrPort = 10000
    destPort = 10001
    
    client = Client(addrPort, destPort)

    client.send_thread.start()
    client.recv_thread.start()

