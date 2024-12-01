# This is the python script that will decode the FSK ascii data

import zmq
import time
import collections
import struct

# config

# variables
socket_loc = "tcp://localhost:4444"
samp_rate = 48000
t_bit = 0.022
sps = int(samp_rate*t_bit)
tol = 3

msg_len = 6
start_sequence = [chr(97),chr(98)]


#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(socket_loc)

# Subscribe to socket
filter = ""
socket.setsockopt_string(zmq.SUBSCRIBE, filter)


count = 0
current_bit = 0
saved_bits = []
saved_byte = b""

old_time = 0
new_time = 0

current_data = b""
count1 = 0
count0 = 0

aligned = False

data = []


# Main Loop
while True:

    # Get new data
    try:
        raw_data = socket.recv(flags=zmq.NOBLOCK)
        current_data += raw_data
    except:
        pass

    # If there is new data to process, count samples    
    while current_data != b"":
        bit = int(struct.unpack('f', current_data[:4])[0])
        current_data = current_data[4:]  
    
        if (count >= sps-tol):
            count = 0
            saved_bits.append(current_bit)
            # print(f"Bit counted!  Now we're at {saved_bits}")
        elif (current_bit == bit):
            count += 1    
        elif (current_bit != bit):
            # print(f"Switching to {bit} from {current_bit} without counting it after {count} samples")
            current_bit = bit
            count = 0


    # Deal with collected bits
    while len(saved_bits) > 8:

        # ensure collected bits start with a zero
        if (saved_bits[0] != 0):
            while (saved_bits[0] != 0):
                saved_bits.pop(0)
                # print("Popping leading 1!")
        else:
            binary_list = [bin(i)[2:] for i in saved_bits[:8]]
            byte_binary = "".join(binary_list)
            mychr = chr(int(byte_binary,2))
            # print(mychr)
            data.append(mychr)

            saved_bits = saved_bits[8:]
        
    # Handle message
    while (len(data) > msg_len):
        msg = data[:msg_len]

        if (msg[:2] != start_sequence):
            data = data[1:]
        else:
            print(f"Receving Message: {"".join(msg[2:])}")

            data = data[msg_len:]

        
        
