import Client
from Client import AppendEntryRPC
from Client import Client
import RPC
from RPC import ClientAppendEntryRPC
from RPC import ClientEntryResponseRPC
import json
import kthread
from mock import patch
import pickle
import socket
import time 
import unittest


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