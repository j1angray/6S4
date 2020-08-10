
import time
import json
import socket
import random
import pickle
import kthread
import unittest

from ..RPC import *
from CandidateActions import *
from mock import patch



class CandidateactionsTest(unittest.TestCase):
    def test_candidate(self):
        self.assertIsInstance(
            Server.candidate(self=<CandidateActions.Server object at 0x10472b0b8>),
            RPC.RequestVoteRPC
        )


    def test_follower(self):
        self.assertEqual(
            Server.follower(self=<CandidateActions.Server object at 0x10472b0b8>),
            'candidate'
        )


    def test_main(self):
        self.assertEqual(
            CandidateActions.main(),
            None
        )


    @patch.object(RequestVoteRPC, '__init__')
    def test_request_vote(self, mock___init__):
        mock___init__.return_value = None
        self.assertIsInstance(
            Server.request_vote(self=<CandidateActions.Server object at 0x10472b0b8>),
            RPC.RequestVoteRPC
        )

'''
if __name__ == "__main__":
    unittest.main()
'''