# This is the python script that will decode the FSK ascii data

#
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import sys
import zmq


#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates...")
socket.connect("tcp://localhost:4444")

# Subscribe to zipcode, default is NYC, 10001
filter = ""
socket.setsockopt_string(zmq.SUBSCRIBE, filter)

# Process 5 updates
while True:
    print(int.from_bytes(socket.recv()[1:10]))