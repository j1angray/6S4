import sys
from Server import *


if __name__ == '__main__':
	ServerId = int(sys.argv[1])
	ServerConfig = "config.json"
	ClientId = 111
	ClientConfig = 10000
	server = Server(ServerId, ServerConfig, ClientId, ClientConfig)
	server.run()