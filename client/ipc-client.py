#!/usr/bin/env python3
# ipc_client.py

import socket

HOST = socket.gethostbyname('ipc_server_dns_name')
PORT = 9898        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for i in range(50):
        s.sendall(str(i).encode())
    data = s.recv(1024)

print('Received', repr(data.decode()))
