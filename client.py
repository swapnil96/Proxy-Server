#!/usr/bin/python

import socket
import os
import sys

size = 4096

def client():
    # Make connection to server 

    try:
        file = open("input.txt", "r") # Open the input file for reading instructions.   
        write_to = file.readline() # Get the name of the required file
        data = write_to # The name should also be in the message that needs to be sent to the server.
        addr = file.readline() # Get the address of the 1st server 
        details = addr.split(' ')
        host = details[0] # Get the ip
        port = int(details[1]) # Get the port
        write_to = write_to[:-1] # Remove newline from the name of the required file.
        data += addr # Add the 1st address to the message 
        for line in file:
            data += line
        
    except:
        print "No file found"
        sys.exit()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Creating a TCP socket.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Same as in server. Make socket to be usable by many others.

    try:
        sock.connect((host,port)) # Connect to the server
        print 'connected'

    except:
        print 'Unable to connect to server', host, port
        sys.exit()

    sock.send(data) # Send the instructions to the main server at ip = 127.0.0.1 and port 10101

    # Recieve the size of the file so that reading could be ended without closing the server socket 
    # Indicator that the file is located. Little bit similar to a SYN_ACK in TCP. 
    SYN_ACK = sock.recv(1024) 
    try: # That the SYN_ACK is an integer. Other wise either the file is not found or any address is not present.
        size = int(SYN_ACK)

    except:
        print SYN_ACK
        sys.exit()

    sock.send('1') # If size is verified as an integer then it sends 1 as an ACK in TCP and then waits for receiving data.
    current_size = 0

    out = open("recieved_" + write_to, "a") # Open a file to write the data
    while current_size <= size: # Reads till the current_size is less than equal to the size sent earlier
        
        data = sock.recv(size)
        if data == '': # Checks for end of data by looking that empty string is sent or not.
            break

        out.write(data)
        current_size += len(data)
        print len(data) # Print the length of each packet to show that data is coming in chunks

    out.close() # close the file.

if __name__ == '__main__':
    sys.exit(client())