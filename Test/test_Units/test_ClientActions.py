
import time
import json
import socket
import random
import pickle
import kthread
import unittest

from Client import *
import RPC import *
from ClientActions import *
from mock import patch



class ClientTest(unittest.TestCase):
    def test_main(self):
        self.assertEqual(
            Client.main(),
            None
        )


    @patch.object(ClientAppendEntryRPC, '__init__')
    @patch.object(ClientEntryResponseRPC, '__init__')
    def test_rpc_process(self, mock___init__, mock___init__):
        mock___init__.return_value = None
        mock___init__.return_value = None
        self.assertIsInstance(
            Client.rpc_process(self=<Client.Client object at 0x1033560f0>),
            RPC.ClientEntryResponseRPC
        )


'''
if __name__ == "__main__":
    unittest.main()
'''
