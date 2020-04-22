import getopt
import os
import signal
import socket
import threading
import run

import commands
from utils import send, set_interaction

# import multiprocessing
# import daemon
# TODO daemon
#
# with daemon.DaemonContext():
#     pass

server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_sockets = []


def KeyboardInterruptHandler(signal, frame):
    server_socket.close()
    for csoc in client_sockets:
        csoc.close()
    print('stop server')
    exit(0)


def command_handler(soc: socket.socket, msg: str):
    print("command (" + msg + ") is handled by a thread")
    cmd = msg.split()[0]
    args = msg.split()[1:]
    # optlist, args = getopt.getopt(args, 'h', ['help'])
    # print(optlist, args)  # TODO
    if cmd == "help" or msg == '\0' or cmd == "-h" or cmd == "--help":
        commands.main_help(soc)  # TODO more intelligent
    elif cmd == "ps":
        commands.ps(soc, args)
    elif cmd == "run":
        commands.run(soc, args)
    elif cmd == "start":
        pass
    elif cmd == "rm":
        commands.rm(soc, args)
    elif cmd == "rmi":
        pass
    elif cmd == "bgrun":
        set_interaction(soc, False)
        run.run(detach=True, cmd=('/usr/sbin/nginx', '-g', 'daemon off;'), image='nginx.img')  # TODO
        send(soc, "detach mode", newline=True)
    elif cmd == "term":
        set_interaction(soc, False)
        run.terminate(args[0])
        send(soc, "should be terminated", newline=True)
    else:
        # pass
        set_interaction(soc, False)
        send(soc, "pass", newline=True)
    soc.close()
    client_sockets.remove(soc)


def main():
    if not os.path.exists('./container'):
        os.mkdir('./container')
    signal.signal(signal.SIGINT, KeyboardInterruptHandler)
    # TODO file socket
    print('start server, pid=' + str(os.getpid()))
    port = 5555
    server_socket.bind(('', port))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        client_sockets.append(client_socket)
        print('connection from', addr)
        msg = client_socket.recv(1024).decode('utf-8')

        # single thread
        # command_handler(msg)

        # multiple thread
        thread = threading.Thread(target=command_handler, args=[client_socket, msg])
        thread.start()
        # multiple process
        # process = multiprocessing.Process(target=command_handler, args=(msg,))
        # process.join()


if __name__ == '__main__':
    main()
