import socket

if __name__ == '__main__':
    port = 5555
    client_socket = socket.socket()
    try:
        client_socket.connect(('127.0.0.1', port))
    except socket.error:
        print("connection is not available")
    else:
        command = input("container$ ")
        # command = "help"
        client_socket.send(command.encode('utf-8'))
        client_socket.close()
