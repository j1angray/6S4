
import time
import json
import socket
import random
import pickle
import kthread
import unittest

from RPC import *
from Server import *
from RPCProcess import *
from mock import patch


class RpcprocessTest(unittest.TestCase):
    @patch.object(Server, 'toFollower')
    def test_RPC_process(self, mock_toFollower):
        mock_toFollower.return_value = None
        self.assertEqual(
            RPCProcess.RPC_process(server=<Server.Server object at 0x10362e668>,msg=<RPC.AppendEntryRPC object at 0x10364a4a8>),
            0
        )


    @patch.object(RequestVoteRPC, '__init__')
    @patch.object(Server, '__init__')
    @patch.object(EntryResponseRPC, '__init__')
    @patch.object(AppendEntryRPC, '__init__')
    @patch.object(VoteResponseRPC, '__init__')
    def test_main(self, mock___init__, mock___init__, mock___init__, mock___init__, mock___init__):
        mock___init__.return_value = None
        mock___init__.return_value = None
        mock___init__.return_value = None
        mock___init__.return_value = None
        mock___init__.return_value = None
        self.assertEqual(
            RPCProcess.main(),
            None
        )

'''
if __name__ == "__main__":
    unittest.main()
'''
