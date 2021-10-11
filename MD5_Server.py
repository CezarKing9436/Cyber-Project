import socket
import select
import pickle
import random
import hashlib

MAX_MSG_LENGTH = 1024
SERVER_PORT = 8826
CONST_ADDITION = 100000

SERVER_IP = socket.gethostbyname(socket.gethostname())
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
def Creat_Hash():
    num_zero = random.randint(1,10)
    number = random.randint(1,10**(10-num_zero)-1)
    print(number)
    print(num_zero)
    string = "0"*num_zero+str(number)
    print(string)
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode())
    digest = md5_hash.hexdigest()
    return digest
HASH = Creat_Hash()
client_sockets = []
CurrentNumber=0
B=True
while B:
    rlist, wlist, xlist = select.select([server_socket]+ client_sockets,client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
            connection.send(HASH.encode())
        else:
            data = current_socket.recv(MAX_MSG_LENGTH).decode()
            print(data)
            if(data == "GetRange"):
                current_socket.send(pickle.dumps(["RANGE_NUMBERS",CurrentNumber,CurrentNumber+CONST_ADDITION]))
                CurrentNumber= CurrentNumber + CONST_ADDITION
            if (data.split()[0] == "FoundNumber"):
                print("the number is "+str(data.split()[1]))
                for client in client_sockets:
                    client.send(pickle.dumps(["FOUND_NUMBER_CLOSE"]))
                    print("X")
                B= False
