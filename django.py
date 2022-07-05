#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 9020         # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                try:
                    path = data.rstrip('\n').rstrip('\r')
                    # GET /api/v1/ HTTP/1.1
                    # Host: localhost
                    print(repr(path))
                    with open(path, 'r') as fd:
                        conn.sendall((fd.read(1000) + '\r\n').encode('utf-8'))
                except Exception as e:
                    conn.sendall(str(e + '\r\n').encode('utf-8'))
    except Exception as e:
        print(e)
    finally:
        s.shutdown(socket.SHUT_RDWR)
