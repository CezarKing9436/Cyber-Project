import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 8826
SERVER_IP = socket.gethostbyname(socket.gethostname())
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
HASH = "f457c545a9ded88f18ecee47145a72c0"

client_sockets = []
count = 1

while True:
    rlist, wlist, xlist = select.select([server_socket]+ client_sockets,client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
            connection.send(HASH.encode())
        else:
            data = current_socket.recv(MAX_MSG_LENGTH)
            if(data == "GetRange"):



    for w in wlist:
        pass