import socket
import threading
import os
import multiprocessing
# import daemon
# TODO daemon
#
# with daemon.DaemonContext():
#     pass


def command_handler(msg):
    print(msg, "handled by pid", os.getpid())
    if msg == "" or msg == "help":
        print("help to be implemented")


def main():
    # TODO file socket
    print('start server, pid=' + str(os.getpid()))
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    port = 5555
    server_socket.bind(('', port))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        print('connection from', addr)
        msg = client_socket.recv(1024).decode('utf-8')
        print('close client socket')
        client_socket.close()

        # single thread
        # command_handler(msg)

        # multiple thread
        thread = threading.Thread(target=command_handler, args=[msg])
        thread.start()
        # multiple process
        # process = multiprocessing.Process(target=command_handler, args=(msg,))
        # process.join()

    print('end progress')
    server_socket.close()


if __name__ == '__main__':
    main()
