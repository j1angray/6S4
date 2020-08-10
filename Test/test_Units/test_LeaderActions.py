
import time
import json
import socket
import random
import pickle
import kthread
import unittest

from ..RPC import *
from LeaderActions import *
from mock import patch


class LeaderactionsTest(unittest.TestCase):
    def test_candidate(self):
        self.assertIsInstance(
            Server.candidate(self=<LeaderActions.Server object at 0x103738198>),
            RPC.RequestVoteRPC
        )


    def test_follower(self):
        self.assertEqual(
            Server.follower(self=<LeaderActions.Server object at 0x103738198>),
            'candidate'
        )


    @patch.object(VoteResponseRPC, '__init__')
    def test_leader(self, mock___init__):
        mock___init__.return_value = None
        self.assertEqual(
            Server.leader(self=<LeaderActions.Server object at 0x103738198>),
            'leader'
        )


    def test_main(self):
        self.assertEqual(
            LeaderActions.main(),
            None
        )


    @patch.object(ClientAppendEntryRPC, '__init__')
    def test_request_entry(self, mock___init__):
        mock___init__.return_value = None
        self.assertIsInstance(
            Server.request_entry(self=<LeaderActions.Server object at 0x103738198>),
            RPC.ClientAppendEntryRPC
        )


    @patch.object(RequestVoteRPC, '__init__')
    def test_request_vote(self, mock___init__):
        mock___init__.return_value = None
        self.assertIsInstance(
            Server.request_vote(self=<LeaderActions.Server object at 0x103738198>),
            RPC.RequestVoteRPC
        )


    @patch.object(AppendEntryRPC, '__init__')
    def test_send_heartbeat(self, mock___init__):
        mock___init__.return_value = None
        self.assertIsInstance(
            Server.send_heartbeat(self=<LeaderActions.Server object at 0x103738198>),
            RPC.AppendEntryRPC
        )

'''
if __name__ == "__main__":
    unittest.main()
'''