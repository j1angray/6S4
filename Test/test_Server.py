import Server
from Server import Server
import __main__
import __main__
import _bootlocale
import codecs
from codecs import BufferedIncrementalDecoder
from codecs import IncrementalEncoder
import json
from json import JSONDecodeError
import kthread
from mock import patch
import pickle
import random
import socket
import sys
import threading
from threading import Barrier
import time
import unittest


class ServerTest(unittest.TestCase):
    @patch.object(Barrier, 'start')
    def test_candidate(self, mock_start):
        mock_start.return_value = None
        self.assertEqual(
            Server.candidate(self=<__main__.Server object at 0x103740208>),
            None
        )


    def test_follower(self):
        self.assertEqual(
            Server.follower(self=<__main__.Server object at 0x103740208>),
            None
        )


    @patch.object(json, 'load')
    @patch.object(_bootlocale, 'getpreferredencoding')
    @patch.object(BufferedIncrementalDecoder, '__init__')
    def test_load_config(self, mock___init__, mock_getpreferredencoding, mock_load):
        mock___init__.return_value = None
        mock_getpreferredencoding.return_value = 'UTF-8'
        mock_load.return_value = {'id': [1, 2, 3], 'port': [10001, 10002, 10003]}
        self.assertEqual(
            Server.load_config(self=<__main__.Server object at 0x103740208>,config='config.json'),
            1
        )


    def test_main(self):
        self.assertEqual(
            __main__.main(),
            None
        )


    @patch.object(Barrier, 'start')
    def test_run(self, mock_start):
        mock_start.return_value = None
        self.assertEqual(
            Server.run(self=<__main__.Server object at 0x103740208>),
            None
        )


    @patch.object(IncrementalEncoder, '__init__')
    @patch.object(_bootlocale, 'getpreferredencoding')
    @patch.object(json, 'dump')
    def test_save_state(self, mock_dump, mock_getpreferredencoding, mock___init__):
        mock_dump.return_value = None
        mock_getpreferredencoding.return_value = 'UTF-8'
        mock___init__.return_value = None
        self.assertEqual(
            Server.save_state(self=<__main__.Server object at 0x103740208>),
            1
        )

'''
if __name__ == "__main__":
    unittest.main()
'''