import  hashlib
import socket
import pickle
import threading
import select
import time



class Worker:
    def __init__(self,socket,Hash):
        self.socket = socket
        self.isWorking = False
        self.HashDecode = Hash

    def GetIsWorking(self):
        return self.isWorking
    def SetIsWorking(self,IsWorking):
        self.isWorking= IsWorking

    def decoder(self,start,end):
        LENGTH_CONST = 11
        for i in range(start,end):
            for j in range(LENGTH_CONST-len(str(i))):
                num = str(i).zfill(j+len(str(i)))
                md5_hash = hashlib.md5()
                md5_hash.update(num.encode())
                digest = md5_hash.hexdigest()
                if (digest == self.HashDecode):
                    self.socket.send(("FoundNumber "+ num).encode())
                    break
        self.isWorking = False

def receive(sock,worker,stop):
    while True:
        rlist, wlist, xlist = select.select([sock], [], [], 0.01)
        if sock in rlist:
            data = pickle.loads(sock.recv(1024))
            print(data)
            if(data[0]=="RANGE_NUMBERS"):
                start, end = data[1],data[2]
                worker.decoder(start,end)
            if(data[0]=="FOUND_NUMBER_CLOSE"):
                stop.set()
                return





def main():
    SERVER_PORT = 8826
    SERVER_IP = socket.gethostbyname(socket.gethostname())
    SELECT_TIMEOUT = 0.01
    sock= socket.socket()
    sock.connect((SERVER_IP, SERVER_PORT))
    hash = sock.recv(1024).decode()
    worker = Worker(sock,hash)
    stop = threading.Event()
    receive_thread = threading.Thread(target=receive,args =[sock,worker,stop])
    receive_thread.start()
    while(not stop.isSet()):
        if(not worker.GetIsWorking()):
            worker.SetIsWorking(True)
            sock.send("GetRange".encode())


if __name__ == "__main__":
    main()