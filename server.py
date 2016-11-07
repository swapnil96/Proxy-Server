#!/usr/bin/python

import socket
import os
import sys
import threading

class Server: # Server class which implements server/proxy

    def __init__(self):

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Re-use the socket 
        self.server_socket.bind((host,port)) # bind the socket to a public host, and a port   
        self.server_socket.listen(4) # Become a server socket and listens to any incoming request

    def main(self):
        # Main loop which will run and look for incoming requests and if a connection is found it will make an another thread.

        while True:
            (client_socket, client_address) = self.server_socket.accept() # Establish the connection
            
            # Initialize a thread to make take care of the connection
            # so that the main server can keep listening to requests
            # target feild is the function that will run in another thread
            # args are the argument for target fucntion
            print "Connection occured from ", client_address
            concurr = threading.Thread(target = self.decide, args = (client_socket, client_address)) 
            
            # Set the thread as daemon so that it stops operating when main thread exits.
            # This assures that no thread should run if any link is broken.
            concurr.setDaemon(True) 

            concurr.start() # Finally start the thread to work concurrently.

    def decide(self, caller_socket, caller_address):
        # This function decides either it will act as server or proxy by reading the file passed by the caller.
        # If only 1 address is present in the reuest than it knows that it has no one to connect so tries to send the requested file.

        # Get the request from the caller, the input file from which the client.
        # The lines contains the IP addresses and the port threfore the size never exceeds 1024 bytes.
        request = caller_socket.recv(1024)
        addresses = request.split('\n')
        # Check if the request contains less than 2 lines which means that it should try to send the requested file mentioned in request.
        # Decides whether to act as server or proxy.
        if len(addresses) <= 2: 
            
            # Try to open the requested file.
            print "Acting as server"
            try:

                # Send the size of file to client so that it can close the connection when file is recieved.
                caller_socket.sendall(str(os.path.getsize(addresses[0]))) 
                ACK = caller_socket.recv(4) # Waits till acknowledgement is received from client that it has got the size.
                file = open(addresses[0], "r")
                caller_socket.sendall(file.read()) # If found then send the file. It would try to send the whole file at one time. 
                caller_socket.close()

            # Send message that file is not found.    
            except:    
                caller_socket.sendall("File not found")
                caller_socket.close()

        else:   
            print "Acting as proxy"
            # Extract the next server/proxy to go, addresses[1] stores address os itself, addresses[2] stores address of next hop.
            details = addresses[2].split(' ') # Separate the IP and port number.
            del addresses[1] # Delete address of itself.
            webserver = details[0] # IP of next hop.
            port1 = int(details[1]) # port of next hop.
            
            final = '' # Modified message to send to next hop.
            
            # Need to send the messsage as a string and to make difference in different lines, we need '\n' between every line.
            for line in xrange(len(addresses)):
                if line == len(addresses) - 1:
                    final += addresses[line]

                else:     
                    final += addresses[line] + '\n'

            self.proxy_thread(webserver, port1, final, caller_socket)            

    def proxy_thread(self, webserver, port1, request, caller_socket):
        # Function which makes the server to work like a proxy.

        # Try to connect with the given webserver and port1
        try:

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket to connect to the next server/proxy.
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Keep socket open for other connections
            sock.connect((webserver, port1))
            sock.sendall(request) # Send the request to the next server/proxy.


            SYN_ACK = sock.recv(1024) # Recieves the size of file from next hop.
            caller_socket.send(SYN_ACK) # Relays the size to the caller_socket.
            ACK = caller_socket.recv(4) # Recieves the acknowledgement from caller_socket that client has got the size.
            sock.send(ACK) # Send the ack to the next hop.
            
            # After it waits and listens to the next hop for the file.
            # Continuously read data from the next server/proxy.
            # This ensures that at every level buffer amount of data is received and not a complete file.
            # Therefore any data that is received from next hop is sent to the previous hop.
            while True:

                data = sock.recv(1024)  # Receive data from next hop till anything is recieved.
                if (len(data) > 0):
                    caller_socket.send(data) # Send the data continuously to the caller_socket without waiting for the whole file.     

                else:
                    break
             
            sock.close() # Close the forward socket as all data has come from there.
            caller_socket.close() # Close the caller's socket as data has been sent to the caller. 

        except:
            print "Socket forming error." # If socket can't be build from the  given argument, might be that port is already used.
            if sock:
                sock.close()

            if caller_socket:
                caller_socket.sendall("Address not found")
                caller_socket.close

if __name__ == "__main__":
    
    host = raw_input("Host - ")
    port = int(raw_input("Port - "))
    server = Server()
    server.main()