
import time
import json
import socket
import random
import pickle
import kthread
from RPC import *


class Server:
    def __init__(self, id, clientId):
        self.id = id
        self.state = "follower"

        #self.peers = []
        #self.voters = []
        self.numVotes = 0
        #self.nodePorts = {}

        self.clientId = clientId
        #self.clientConfig = clientConfig

        #self.load_config(config)
        
        self.currentTerm = 0
        self.VoteFor = -1
        self.log = {}

        self.lastLogIndex = 0
        self.lastLogTerm = 0

        self.timeOut = random.uniform(1, 3)

        '''Socket'''
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.bind(("",self.port))
        
        '''Threads'''
        #self.follower_state = kthread.KThread(target=self.follower, args= ())
        #self.candidate_state = kthread.KThread(target=self.candidate, args= ())
        #self.leader_state = kthread.KThread(target = self.leader, args = ())     

        #self.rpc_load = kthread.KThread(target = self.rpc_socket, args = (RPC_process,))

        #self.vote_call = kthread.KThread(target = self.request_vote, args =())
        #self.heartbeat_call = kthread.KThread(target = self.send_heartbeat, args =())
        #self.entry_call = kthread.KThread(target = self.request_entry, args =())

    def follower(self):

        #print("Node[{}]: Follower. / {} /".format(self.id, time.asctime()))
        self.state = "follower"
        self.last_update = time.time()
        time_out = self.timeOut

        while time.time() - self.last_update < time_out:
            pass
        self.state = "candidate"
        return (self.state)

        while True:
            try:          
                self.last_update = time.time()
                while time.time() - self.last_update < self.timeOut: 
                    pass
                self.state = "candidate"
                return (self.state)
            except Exception as e:
                print(e)

    def candidate(self):
        self.state = "candidate"
        #if len(self.peers) >= 0:
        self.currentTerm += 1
        self.votefor = self.id
        self.numVotes = 1
        return (self.request_vote())

    def request_vote(self):

        data = str(self.lastLogTerm) + " " + str(self.lastLogIndex)
        msg = RequestVoteRPC(self.id, 2, self.currentTerm, data)
        #self.send_socket(msg, self.nodePorts[peer])
        return(msg)
  

    def leader(self):

        reply = VoteResponseRPC(2, 1, self.currentTerm, 1)

        self.numVotes = 2

        #print("\n<Term Update>: Term {}'s Leader[{}]. / {} /\n".format(self.currentTerm, self.id, time.asctime()))
        self.state = "leader"
        #self.save_state()
        self.send_heartbeat()
        self.request_entry()
        return (self.state)

    def send_heartbeat(self):

        self.state = "leader"
        msg = AppendEntryRPC(1, 2, self.currentTerm, self.lastLogIndex)
        return msg

    def request_entry(self):

        self.state = "leader"
        msg = ClientAppendEntryRPC(1, 111, self.currentTerm, self.lastLogIndex, 'Leader')
        return msg







