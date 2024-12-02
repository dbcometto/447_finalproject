# This is version 2 of decoding an FSK stream

import zmq
import time
import threading
import numpy as np
import queue
import random

dataq = queue.Queue()

socket_loc = "tcp://localhost:4444"

def consumer(exit_flag):
    consumer_id = random.randrange(1, 10005)
    print("I am consumer #%s" % (consumer_id))
    context = zmq.Context()
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect(socket_loc)
    while True:
        dataq.put(consumer_receiver.recv())
        # Exit flag?
        if exit_flag():
            consumer_receiver.close()
            time.sleep(0.5)
            context.term()
            time.sleep(0.5)
            break

def main():
    exit_flag = False
    # Set up multithreading
    rxThread = threading.Thread(target=consumer, args=(lambda: exit_flag,))
    rxThread.daemon = True
    rxThread.start()  # Start the receive thread
    i = 0
    wait_counter = 0
    while True:
        print("thinking")
        try:
            if dataq.empty() and (i > 0):  # Assume we've received all the data
                if wait_counter < 20:  # 20 is an arbitrary number, 20×0.1s = 2s
                    wait_counter += 1
                    time.sleep(0.1)
                    print("waiting")
                else:  # Might need to do some data cleanup here
                    print("Data queue is empty and I'm exiting")
                    exit_flag = True
                    break
            else:
                wait_counter = 0  # Reset the wait counter if we've been waiting
                buff = dataq.get()
                data = np.frombuffer(buff, dtype="float32")
                print(data)
        except:
            pass



# Run code
print("Starting main loop!")
while True:
    main()
