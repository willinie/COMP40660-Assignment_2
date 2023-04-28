#!/usr/bin/env python3
# ipc_client.py

import socket

HOST = socket.gethostbyname('ipc_server_dns_name')
PORT = 9898        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
#    s.sendall(b'Hello, world. IPC success!')
    for i in range(50):
        s.sendall(str(i).encode())
        data = s.recv(1024)

#print('Received', repr(data))
        print('Received', repr(data.decode()))
        
    avg = s.recv(1024)
    med = s.recv(1024)
    sd = s.recv(1024)
    
    print("Received " + "Average: " + str(avg) + ", Median: " + str(med) + ", Stdev: " + str(sd))
