# Proxy-Server
Server acts as proxies or shares files.

A server-client program that achieves the following: 
1) Server listens on a port.
2) Client makes a TCP connection and server sends a file to the client. 
3) In addition to acting as a server, the server can also act like a proxy.

The solution have two parts: a server program and a client program. 
The server program is run with port number, IP address as an input. It listens at the specified port for 
incoming connections and can function as either a proxy or a file server depending on the request made by the client.
The client program is run with an input file in the following format:

filename
proxy1-ip-address/hostname port
proxy2-ip-address/hostname port
proxy3-ip-address/hostname port
...
proxyn-ip-address/hostname port
server-ip-address/hostname port
