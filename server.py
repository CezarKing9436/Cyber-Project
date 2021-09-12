import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 8826
SERVER_IP = socket.gethostbyname(socket.gethostname())
print("Setting up server DUDUSH...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("SERVER DUDUSH Listening for clients...")


client_sockets = {}
messages_to_send = []
count = 1
groups = [()]

while True:
    rlist, wlist, xlist = select.select([server_socket]+ list(client_sockets.keys()), list(client_sockets.keys()), [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets[connection] = ","
            count += 1
        else:
            print("Data from existing client")
            data = current_socket.recv(MAX_MSG_LENGTH).decode()
            print(data + " that is the data")
            if(data.split("/")[0]=="NAME_SOCK"):
                print(data.split("/")[2])
                print(list(client_sockets.values()))
                print(data.split("/")[2] in list(client_sockets.values()) )
                if data.split("/")[2] not in list(client_sockets.values()):
                    print("a")
                    client_sockets[current_socket] = data.split("/")[2]
                    current_socket.send("NAME_SOCK_STOP".encode())
                else:
                    current_socket.send("NAME_SOCK".encode())
            elif data.split("/")[0] == "quit":
                print("Connection closed", )
                info = data.split("/")
                info.append(info[1]+ " "+info[2]+" has left the server")
                info = '/'.join([str(elem) for elem in info])
                print(info)
                #messages_to_send.append((current_socket,client_sockets[current_socket], "has left the chat",list(client_sockets.keys()).copy()))
                for key in client_sockets:
                    key.send(info.encode())
                del client_sockets[current_socket]
                current_socket.close()
            elif data.split("/")[0]=="CREATE_GRUOP":
                names = ""
                print("fuck")
                for name in client_sockets:
                    names=names+ client_sockets[name]+ "/"
                names = names[0:len(names)-1]
                print(names+ " that are the names")
                current_socket.send(names.encode())
            elif data.split("/")[0]=="CREATE_GRUOP_FOR_OTHERS":
                names_list = data.split("/")[1].split("*")
                for name in names_list:
                    sock = list(client_sockets.keys())[list(client_sockets.values()).index(name)]
                    print(data.split("/")[2])
                    sock.send(str("CREATE_GRUOP_FOR_OTHERS"+"/"+"/"+"/"+data.split("/")[2]+"/"+"/"+client_sockets[current_socket]).encode())#data.split("/")[2] group name

                    # index = list(client_sockets.values()).index(name)
                    # print(index)
                    # client_temp = list(client_sockets.keys())[index]
                    # print(client_temp)
                    # print(type(client_temp))
                    # client_temp.send(str("CREATE_GRUOP_FOR_OTHERS"+"/"+"/"+data.split[2]).encode())
                groups.append((names_list,client_sockets[current_socket],data.split("/")[2]))
            elif data.split("/")[0]=="DEL_MEMBER_OF_GROUP":
                names_list = data.split("/")[1].split("*")
                print(names_list)
                for name in names_list:
                    sock = list(client_sockets.keys())[list(client_sockets.values()).index(name)]
                    print(sock)
                    print(type(sock))
                    sock.send(str("DEL_MEMBER_OF_GROUP"+"/"+"/"+"/"+data.split("/")[2]+"/"+"/"+client_sockets[current_socket]).encode())

            else:
                print(data)
                messages_to_send.append((current_socket,client_sockets[current_socket],data,list(client_sockets.keys()).copy()))


    for msg in messages_to_send:
        client, value, data, client_sockets_temp = msg
        for client_socket in client_sockets_temp:
            if client_socket in wlist and client_socket is not client:
                client_socket.send((str(data).encode()))
                print("data sent")
                index = messages_to_send.index(msg)
                messages_to_send[index][3].remove(client_socket)
                if (len(messages_to_send[index][2]) == 1):
                    messages_to_send.remove(messages_to_send[index])