# 654 Project


### Set up

1. Modify the script written in the run.sh file, change the Folder address after the cd command to corresponding local path.

2. The port of each socket of node is bound to are given in the config.json file. Each node corresponds to a port and the number of nodes can be added (preferably odd).



### Operation guidance

1. After entering the specified folder in terminal, then run the run.sh file.

2. Multiple terminal windows will be generated to simulate distrubuted nodes which will contain multiple servers and a single client.

3. Manually shutdown one terminal window to see how Raft consensus protocol works by reading the print information of RPC communication.



### File generation

1. Election information includes updates on term and leader will appear in the Election folder as json files.

2. Records about log replication about the number of updates requested by the client will appear in the Log folder as json files.
