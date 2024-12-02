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

use_overhead = False
fix_leading_zero = False
msg_len = 20
start_sequence_length = 2
start_sequence = [chr(97),chr(98)]

count = 0
current_bit = 0
saved_bits = [0]
saved_byte = b""

old_time = 0
new_time = 0

current_data = b""
count1 = 0
count0 = 0

data = []

debugging = False


#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(socket_loc)

# Subscribe to socket
filter = ""
socket.setsockopt_string(zmq.SUBSCRIBE, filter)

print(f" I am setup and waiting for messages on {socket_loc}")


mycount = 0
maxcount = 16


# Main Loop
with open("samples2.dat", "rb") as file:
    for line in file:
        raw_data = line.strip()
        current_data += raw_data
        print(current_data[0])
        print(len(current_data))

        # If there is new data to process, count samples    
        while len(current_data)>4:
            bit = int(struct.unpack('f', current_data[:4])[0])
            current_data = current_data[4:] 
            print(f"Taking a byte!  Bytes left are {len(current_data)/4}")

            if (count >= sps-tol):
                count = 0
                saved_bits.append(current_bit)
                if debugging:
                    print(f"Bit counted!  Now we're at {saved_bits}")
            elif (current_bit == bit):
                count += 1    
            elif (current_bit != bit):
                if debugging:
                    print(f"Switching to {bit} from {current_bit} without counting it after {count} samples")
                current_bit = bit
                count = 0


        # Deal with collected bits
        while len(saved_bits) > 8:

            # ensure collected bits start with a zero
            if (saved_bits[0] != 0 and fix_leading_zero):
                while (saved_bits[0] != 0):
                    saved_bits.pop(0)

                    if debugging:
                        print("Popping leading 0!")
            else:
                binary_list = [bin(i)[2:] for i in saved_bits[:8]]
                byte_binary = "".join(binary_list)
                mychr = chr(int(byte_binary,2))
                if debugging:
                    print(mychr)
                data.append(mychr)

                saved_bits = saved_bits[8:]
            
        # Handle message
        if use_overhead:
            while (len(data) > msg_len):
                msg = data[:msg_len]

                if (msg[:2] != start_sequence):
                    print(f"Attempted Message: {"".join(msg)}")
                    data = data[1:]
                else:
                    print(f"Receving Message: {"".join(msg[2:])}")

                    data = data[msg_len:]
        else:
            while (len(data) > 0):
                print(f"Received Char: {data[0]}")
                data = data[1:]
            
            
