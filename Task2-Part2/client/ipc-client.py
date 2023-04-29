#!/usr/bin/env python3
# ipc_client.py

import os
import rsa
import socket

HOST = socket.gethostbyname('ipc_server_dns_name')
PORT = 9898        # The port used by the server
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Connected by', HOST)

    received = s.recv(BUFFER_SIZE).decode()
    print("[socket]HEADER received")
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)
    print(f"public key info: {filename} -- {filesize}bytes")

    # receive public key
    with open(filename, "wb") as f:
        bytes_read = s.recv(filesize)
        # write to the file the bytes just received
        f.write(bytes_read)
        print("[socket]public key received")

    # print public key
    with open(filename, "r") as f:
        print(f.read())

    # input secret message
    msg = "This is a secret message! Don't share it with anyone."
    print(f"[message] -- {msg}")

    # load public key
    with open(filename, "rb") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())

    # encrypt with public key
    encrypted_msg = rsa.encrypt(msg.encode(), public_key)
    print("[message]encrypted with public key")

    # send encrypted message
    s.sendall(encrypted_msg)
    print("[socket]encrypted message sent to server")


