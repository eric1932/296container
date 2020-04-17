#!/usr/bin/env python3
import signal
import socket
import sys
import os

import utils

client_socket = socket.socket()


def KeyboardInterruptHandler(signal, frame):
    client_socket.close()
    exit(0)


def recv_args(soc: socket.socket) -> {str: str}:
    args = {}
    while True:
        body_length = soc.recv(4).decode()
        if body_length == "next":
            break
        body_length = int(body_length)
        k, v = soc.recv(body_length).decode().split("=")
        try:  # try to convert to int
            v = int(v)
        except ValueError:
            pass  # do nothing
        args[k] = v
    return args


if __name__ == '__main__':
    if os.getuid() != 0:
        print("Error: must run as root")
        client_socket.close()
        exit(1)
    port = 5555
    try:
        client_socket.connect(('127.0.0.1', port))
    except socket.error:
        print("connection is not available")
        client_socket.close()
        exit(1)

    signal.signal(signal.SIGINT, KeyboardInterruptHandler)

    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
    else:
        sys.stderr.write("\033[33m" + "warning: no argument is given; read from input\033[39m\n")
        command = input("container$ ")
    if command == "":  # replace empty string
        command = '\0'
    # command = "help"
    # send command
    client_socket.send(command.encode('utf-8'))
    # receive output & enter interactive mode
    interaction = int(client_socket.recv(4).decode()[-2])
    if not interaction:
        while True:
            buf = client_socket.recv(1024).decode()
            if not buf:
                break
            print(buf, end='')
        client_socket.close()
    else:
        # receive args
        args = recv_args(client_socket)
        client_socket.close()
        utils.run(uuid=args.get("uuid", None), load=args.get("load", False))
