
import time
import math
import json
import socket
import random
import pickle
import kthread
from Server import *
from RPC import *
import sys


def RPC_process(server, msg):

    type = msg.type
    term = msg.term
    sender = msg.src
    receiver = msg.dest
    
    if type == 'RequestVote': 
        print("<Vote Request>: Candidate: Node[{}] ———> followers. / {} /".format(sender, time.asctime()))
        if sender not in server.peers:
            return
        if term < server.currentTerm:
            voteGranted = 0
        elif term > server.currentTerm:
            server.toFollower(term)
            voteGranted = 1
            server.VoteFor = sender
            
        else:
            if server.VoteFor == -1 or sender:
                voteGranted = 1
            else:
                voteGranted = 0

        #replyPorts = server.nodePorts[sender]
        #replyMsg = VoteResponseRPC(server.id, sender, server.currentTerm, voteGranted)
        #server.send_socket(replyMsg, replyPorts)
        return(voteGranted)

    elif type == 'VoteResponse': 
        print("<Vote Response>: follower[{}] ———> Candidate[{}]. / {} /".format(sender, receiver, time.asctime()))

        voteGranted = msg.data

        if voteGranted == 1:
            if server.state == "candidate":
                server.voters.remove(sender)
                server.numVotes += 1
                if server.numVotes >= math.ceil(len(server.peers) / 2):
                    server.vote_call.kill() 
                    server.state = "leader"
                    server.follower_state.kill()
                    server.leader_state = kthread.KThread(target = server.leader, args = ())
                    server.leader_state.start()
                    
        else:
            if term > server.currentTerm and server.state == "candidate":
                server.toFollower(term)
        return(server.numVotes)

    elif type == 'AppendEntry':
        print("<Heartbeat> Leader[{}] ———> follower[{}]. / {} /".format(sender, receiver, time.asctime()))

        if term >= server.currentTerm:
            server.toFollower(term)
            if server.state == "follower":
                server.last_update = time.time()
            success = "True"
        else:
            success = "False"

        server.lastLogIndex = msg.lastLogIndex
        #replyPorts = server.nodePorts[sender]
        #replyMsg = EntryResponseRPC(server.id, sender, server.currentTerm, success)
        #server.send_socket(replyMsg, replyPorts)
        return(server.lastLogIndex)

    elif type == 'EntryResponse':
        if msg.success == "True":
            print("<Heartbeat Response> follower[{}] ———> Leader[{}]. / {} /".format(sender, receiver, time.asctime()))
        else:
            if term > server.currentTerm:
                server.toFollower(term)
        return(msg.success)

    elif type == 'ClientEntryResponse':
        print("\n<Client Append Entry> Client[{}] ———> Leader[{}], Log Entry[{}]. / {} /\n".format(sender, receiver, msg.lastLogIndex, time.asctime()))
        
        server.lastLogIndex = msg.lastLogIndex

        log = {}
        log["Client"] = sender
        log["Leader"] = receiver
        log["Index"] = msg.lastLogIndex

        server.log = log

        return(log)

        #logPath = "./Log/log"+str(msg.lastLogIndex)+".json"

        #with open(logPath, "w") as f:
            #json.dump(log, f)

        #if term > server.currentTerm:
            #pass








