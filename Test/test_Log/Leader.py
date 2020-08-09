
import time 
import json
import socket
import kthread


class Leader():
    def __init__(self, src, dest, foll):
        self.src = src # 10001
        self.dest = dest # 10000
        self.foll = foll # 10002

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("",self.src))

        self.send_thread = kthread.KThread(target=self.send, args= ())
        self.recv_thread = kthread.KThread(target=self.recv, args= ())

        self.heartbeat_call = kthread.KThread(target=self.send_heartbeat, args= ())

        self.lastLogIndex = 0


    def send(self):
        while True:
            data = {'success': 'success'}

            print('<Client Entry Response>:commit log[{}] {}. / {} /'.format(self.lastLogIndex, data['success'], time.asctime()))

            data = json.dumps(data).encode('utf-8')

            self.sock.sendto(data, ("", self.dest))

            time.sleep(5) 

             

    def recv(self):
        while True:

            data, addr = self.sock.recvfrom(1024)

            data = json.loads(data)

            if data['type'] == 'ClientAppendEntry':

                self.lastLogIndex = data['index']

                print('\n<Append Entry from Client>: Log[{}]. / {} /'.format(self.lastLogIndex, time.asctime()))

                logPath = './Log/log'+str(self.lastLogIndex)+'.json'

                with open(logPath, 'w') as f:
                    json.dump(data, f)

            elif data['type'] == 'HeartbeatResponse' and data['state'] == 'alive':

                print('\n<Heartbeat Response from follower>. / {} /'.format(time.asctime()))


    def send_heartbeat(self):
        while True:
            try:
                data = {'type': 'heartbeat', 'lastLogIndex': self.lastLogIndex}
                data = json.dumps(data).encode('utf-8')
                self.sock.sendto(data, ("", self.foll))
                time.sleep(1)
            except Exception as e:
                print(e)




if __name__ == '__main__':
    
    selfPort = 10001
    follPort = 10002
    destPort = 10000

    leader = Leader(selfPort, destPort, follPort)

    leader.recv_thread.start()
    leader.send_thread.start()
    leader.heartbeat_call.start()
