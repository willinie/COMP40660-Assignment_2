#!/usr/bin/env python3
# ipc_server.py

import os
import rsa
import socket

HOST = socket.gethostbyname('ipc_server_dns_name')
PORT = 9898        # Port to listen on (non-privileged ports are > 1023)
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

# generate rsa key pair
public_key, private_key = rsa.newkeys(1024)
print("[rsa-key]generated")

# write into file
with open("public.pem", "wb") as f:
    f.write(public_key.save_pkcs1("PEM"))
with open("private.pem", "wb") as f:
    f.write(private_key.save_pkcs1("PEM"))
print("[rsa-key]saved to files")

# Networking
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    with conn:
        print('Connected by', addr)
        public_key_size = os.path.getsize("public.pem")
        # send public key file name and size as a HEADER
        conn.send(f"public.pem{SEPARATOR}{public_key_size}".encode())
        print("[socket]HEADER sent")
        with open("public.pem", "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                conn.sendall(bytes_read)
            print("[socket]public key sent")

        # receive encrypted message
        encrypted_msg = conn.recv(BUFFER_SIZE)
        print("[socket]encrypted message received")

        # decrypt message
        msg = rsa.decrypt(encrypted_msg, private_key).decode()
        print(f"[message]decrypted -- {msg}")