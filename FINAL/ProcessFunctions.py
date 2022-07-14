import os
FORMAT = "utf-8"
SIZE = 8192

def cls():
    os.system('cls')

def waitForInput():
    input("Press ENTER to continue...")

def sendMsg(s, *listMsg):
    for i in listMsg:
        s.sendall(bytes(i, FORMAT))

def recvMsg(s):
    return s.recv(SIZE).decode(FORMAT)

def fromClient(conn):
    print(f"From client {conn.getpeername()}:")

def showRecvData(*list):
    for i in list:
        print(i)