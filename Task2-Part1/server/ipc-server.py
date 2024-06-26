#!/usr/bin/env python3
# ipc_server.py

import socket
import statistics

HOST = socket.gethostbyname('ipc_server_dns_name')
PORT = 9898        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    received = []
    with conn:
        print('Connected by', addr)
        for i in range(50):
            data = conn.recv(1024)
            received.append(int(data.decode()))
            conn.sendall(data)
        
#        print(received)

        # once all the data has been received from client
        avg = statistics.mean(received)
        med = statistics.median(received)
        sd = statistics.stdev(received)

        # encode to binary to send to client
        conn.recv(1024)
        conn.sendall(str(avg).encode())
        conn.recv(1024)
        conn.sendall(str(med).encode())
        conn.recv(1024)
        conn.sendall(str(sd).encode())
        print("Sent " + "Average: " + str(avg) + ", Median: " + str(med) + ", Stdev: " + str(sd))
