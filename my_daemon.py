import os
import signal
import socket
import threading

from commands2.help import Help
from commands2.images import Images
from commands2.ps import Ps
from commands2.rm import Rm
from commands2.run import Run
from commands2.stop import Stop
from utils import send
from utils import set_interaction

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
        # commands.main_help(soc)  # TODO more intelligent
        Help(soc)
    elif cmd == "stop-server":
        set_interaction(soc, False)
        os.kill(os.getpid(), signal.SIGINT)
    elif cmd == "ps":
        Ps(soc, args)
    elif cmd == "run":
        Run(soc, args)
    elif cmd == "rm":
        Rm(soc, args)
    elif cmd == "stop":
        Stop(soc, args)
    elif cmd == "images":
        Images(soc, args)
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
