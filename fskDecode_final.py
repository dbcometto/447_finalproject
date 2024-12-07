# This is the python script that will decode the FSK ascii data using push/pull

import zmq
import struct
import sys

# config
debugging = False
debugging2 = False
verbose = False

# variables
socket_loc = "tcp://localhost:4444"
samp_rate = 48000
t_bit = 0.016
sps = int(samp_rate*t_bit)
tol = 0
tol_other = 30

count = 0
count_other = 0
current_bit = 0
saved_bits = []
saved_byte = b""
current_data = b""
data = []


#  Set up socket to talk to GNU Radio
context = zmq.Context()
pull_socket = context.socket(zmq.PULL)
pull_socket.connect(socket_loc)

print(f" I am setup and waiting for messages on {socket_loc} with {sps} SPS")


# Main Processing Loop
while True: 

    # Get new data
    try:
        raw_data = pull_socket.recv(flags=zmq.NOBLOCK)
        current_data += raw_data
    except:
        pass   

    # If there is new data to process, count samples    
    while len(current_data) >= 4:
        bit = int(struct.unpack('f', current_data[:4])[0])
        current_data = current_data[4:] 
        count += 1

        if (current_bit != bit):
            count_other += 1
            if debugging:
                print(f"Sample not counted!  count_other: {count_other} at count: {count}")

        if (count_other >= tol_other):
            if debugging2:
                print(f"Switching to {current_bit} from {bit} at count: {count}", end = "")

            current_bit = bit
            count_other = 0

            if debugging2:
                print(f"and newcount: {count}")
            
        
        elif (count >= sps-tol):
            if debugging2:
                print(f"Bit counted at count: {count}!",end="")
            count = 0
            count_other = 0
            saved_bits.append(current_bit)
            if debugging2:
                print(f"  Now we're at {saved_bits}")

        


    # Deal with collected bits
    while len(saved_bits) >= 8:

        binary_list = [str(i) for i in saved_bits[:8]]
        byte_binary = "".join(binary_list)
        if debugging:
            print(f"Received Byte: {byte_binary}")

        myint = int(byte_binary,2)
        mychr = chr(myint)

        data.append(mychr)
        saved_bits = saved_bits[8:]
        
    # Handle message
    while (len(data) > 0):
        if verbose:
            print(f"Received Char: {data[0]}")
        else:
            print(data[0], end="")
            sys.stdout.flush()

        data = data[1:]

        
        
