import os
import signal
import socket
import threading

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


def send(soc: socket.socket, msg, delim='\n'):
    soc.send((str(msg) + delim).encode())


def command_handler(soc: socket.socket, msg: str):
    print("command (" + msg + ") is handled by a thread")
    if msg == '\0' or msg == "help":
        send(soc, "i=0;", delim='')
        send(soc, "commands: help exit run ps")
    elif msg == "run":
        send(soc, "i=1;", delim='')
    elif msg == "ps":
        send(soc, "i=0;", delim='')
        send(soc, "UUID\t\tIMAGE\tCOMMAND\tCREATED\tSTATUS")
        for x in os.listdir("./container"):
            if os.path.isfile(os.path.join('container', x)):
                send(soc, x[:-4][:8])
    else:
        # pass
        send(soc, "i=0;", delim='')
        send(soc, "pass")
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
        print('close client socket')

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
