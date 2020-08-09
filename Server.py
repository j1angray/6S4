
import time
import json
import socket
import random
import pickle
import kthread
from RPC import *


class Server:
    def __init__(self, id, config, clientId, clientConfig):
        self.id = id
        self.state = "follower"

        self.peers = []
        self.voters = []
        self.numVotes = 0
        self.nodePorts = {}

        self.clientId = clientId
        self.clientConfig = clientConfig

        self.load_config(config)
        
        self.currentTerm = 0
        self.VoteFor = -1
        self.log = {}

        self.lastLogIndex = 0
        self.lastLogTerm = 0

        self.timeOut = random.uniform(1, 3)

        # socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("",self.port))

        # initial threads
        self.follower_state = kthread.KThread(target=self.follower, args= ())

        self.rpc_load = kthread.KThread(target = self.rpc_socket, args = (RPC_process,))



    def load_config(self, config):

        configs = json.load(open(config))
        ports = configs["port"]
        ids = configs["id"]

        self.port = ports[self.id - 1]

        self.nodePorts = {}
        for nid in ids:
            self.nodePorts[nid] =  ports[nid - 1]
            if nid != self.id:
                self.peers.append(nid)


    def send_socket(self, msg, recv):
        self.sock.sendto(pickle.dumps(msg), ("", recv))

    def recv_socket(self):
        return self.sock.recvfrom(1024)


    def rpc_socket(self, process):
        while True:
            try:
                data, addr = self.recv_socket()
                rpc_msg = pickle.loads(data)
                rpc_thread = kthread.KThread(target = process, args = (self, rpc_msg))
                rpc_thread.start()
            except Exception as e:
                print(e)

        self.sock.close()

    def term_thread(self, thrd):
        if thrd.is_alive():
            thrd.terminate()

    def save_state(self):
        clusterState = {}
        electionPath = './Election/Term'+str(self.currentTerm)+'.json'
        
        clusterState['leader'] = self.id 
        clusterState['followers'] = self.peers
        clusterState['term'] = self.currentTerm
        
        with open(electionPath, 'w') as f:
            json.dump(clusterState, f)


    def follower(self):
        print("Node[{}]: Follower. / {} /".format(self.id, time.asctime()))
        self.state = "follower"
        self.last_update = time.time()
        time_out = self.timeOut
        while time.time() - self.last_update < time_out:
            pass
        #self.kill_thread(self.vote_call)
        self.candidate_state = kthread.KThread(target=self.candidate, args= ())
        self.candidate_state.start()
        #self.candidate()
        while True:
            try:          
                self.last_update = time.time()
                while time.time() - self.last_update < self.timeOut: 
                    pass
                #self.kill_thread(self.vote_call)
                self.candidate_state = kthread.KThread(target=self.candidate, args= ())
                self.candidate_state.start()
                #self.candidate()
            except Exception as e:
                print(e)
  

    def candidate(self):
        self.state = "candidate"
        print("Node[{}]: Candidate. / {} /".format(self.id, time.asctime()))
        if len(self.peers) >= 0:
            self.currentTerm += 1
            self.votefor = self.id
            self.numVotes = 1
            self.vote_call = kthread.KThread(target = self.request_vote, args =())
            self.vote_call.start()


    def leader(self):
        
        self.state = "leader"
        print("\n<Term Update>: Term {}'s Leader[{}]. / {} /\n".format(self.currentTerm, self.id, time.asctime()))
        self.save_state()
        self.heartbeat_call = kthread.KThread(target = self.send_heartbeat, args =())
        self.heartbeat_call.start()
        self.entry_call = kthread.KThread(target = self.request_entry, args =())
        self.entry_call.start()


    def toFollower(self, term):
        self.currentTerm = term

        if self.state == "candidate":

            self.term_thread(self.vote_call)
            self.term_thread(self.candidate_state)

            self.follower_state = kthread.KThread(target=self.follower, args= ())
            self.follower_state.start()

        elif self.state == "leader":

            self.term_thread(self.heartbeat_call)
            self.term_thread(self.entry_call)
            self.term_thread(self.leader_state)
            
            self.follower_state = kthread.KThread(target=self.follower, args= ())
            self.follower_state.start()


    def request_vote(self):

        print("<Election Timeout>: Candidate[{}] update election to term[{}].".format(self.id, self.currentTerm, time.asctime()))
        self.state = "candidate"
        self.voters = self.peers.copy()
        while True:
            try:
                for peer in self.peers:
                    if peer in self.voters:
                        data = str(self.lastLogTerm) + " " + str(self.lastLogIndex)
                        msg = RequestVoteRPC(self.id, peer, self.currentTerm, data)
                        self.send_socket(msg, self.nodePorts[peer])
                time.sleep(2)
            except Exception as e:
                print(e)
            

    def send_heartbeat(self):

        self.state = "leader"
        while True:
            try:
                for peer in self.peers:
                    msg = AppendEntryRPC(self.id, peer, self.currentTerm, self.lastLogIndex)
                    self.send_socket(msg, self.nodePorts[peer])

                time.sleep(2)
            except Exception as e:
                print(e)


    def request_entry(self):

        self.state = "leader"
        #clientId = 111
        #clientConfig = 10000
        #print("\n —————————————————— Log Replication —————————————————— \n")
        while True:
            try:
                msgClient = ClientAppendEntryRPC(self.id, self.clientId, self.currentTerm, self.lastLogIndex, self.port)
                self.send_socket(msgClient, self.clientConfig)

                time.sleep(2)
            except Exception as e:
                print(e)


    def run(self):
        #print("\n —————————————————— Leader Selection —————————————————— \n")
        self.rpc_load.start()
        self.follower_state.start()




