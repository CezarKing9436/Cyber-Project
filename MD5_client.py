import  hashlib
import socket




class Worker:
    def __init__(self,socket,Hash):
        self.socket = socket
        self.isWorking = False
        self.HashDecode = Hash

    def GetWork(self):
        self.socket.send("GetRange".encode())

    def GetIsWorking(self):
        return self.isWorking

    def decoder(self,start,end):
        for i in range(1000):
            md5_hash = hashlib.md5()
            md5_hash.update(str(i).encode())
            digest = md5_hash.hexdigest()
            if (digest == self.HashDecode):
                print("niceee")
                print("the number is " + str(i))
                break


def main():
    SERVER_PORT = 8826
    SERVER_IP = socket.gethostbyname(socket.gethostname())
    SELECT_TIMEOUT = 0.01
    sock= socket.socket()
    sock.connect((SERVER_IP, SERVER_PORT))
    hash = sock.recv(1024).decode()
    print(hash)
    worker = Worker(sock,hash)

if __name__ == "__main__":
    main()


