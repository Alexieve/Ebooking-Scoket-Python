import socket
import json
import os

IP = "127.0.0.1"
PORT = 1234
ADDR = (IP, PORT)
FORMAT = 'utf-8'
SIZE = 1024

###### Processing code #####
# 0 Exit
# 1 Check login
# 2 Add account
# 3 ...
# 4 ...

##### CLASS #####
class users:
    def __init__(self, username, password, cardID):
        self.username = username
        self.password = password
        self.cardID = cardID
class dataBase:
    listUser = []

##### PROCESS FUNCTIONS #####
def cls():
    os.system('cls')
def waitForInput():
    input("Press ENTER to continue...")
def showRecvData(*list):
    print("From client:")
    for i in list:
        print(i)
def sendMsg(s, *listMsg):
    for i in listMsg:
        s.sendall(i.encode(FORMAT))
def recvMsg(s):
    return s.recv(SIZE).decode(FORMAT)
def checkExistAccount(dataServer, username):
    for i in dataServer.listUser:
        if (i.username == username):
            return True
    return False

### MAIN FUNCTIONS ###
def addAccount(s, dataServer): #BUG
    print("Adding account to database...")
    while True:
        username = recvMsg(s)
        showRecvData(username)
        exits = checkExistAccount(dataServer, username)
        if (exits == True):
            print("Account exitst!")
            sendMsg(s, "True")
            continue
        password = recvMsg(s)
        cardID = recvMsg(s)
        showRecvData(password, cardID)
        dataServer.listUser.append(users(username, password, cardID))
        saveDatabase(dataServer)
    print("Adding account complete!")

def checkLogin(s, dataServer):
    print("Checking login of client...")
    username = recvMsg(s)
    password = recvMsg(s)
    showRecvData(username, password)
    for i in dataServer.listUser:
        if (username == i.username and password == i.password):
            sendMsg(s, "True")
            print("Checking complete!")
            return
    sendMsg(s, "False")
    print("Checking complete!")
def saveDatabase(dataServer):
    print("Saving database...")
    with open('data.txt', 'w') as writeFile:
        json.dump(dataServer, writeFile)
    print("Saving complete!")
def loadDatabase(dataServer):
    print("Loading database...")
    with open("data.json", "r") as readFile:
        dataStr = json.load(readFile)
        for i in dataStr['users']:
            dataServer.listUser.append(users(i['username'], i['password'], i['cardID']))
    print("Loading complete!")

##### MAIN #####
def main():
    dataServer = dataBase
    loadDatabase(dataServer)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        cls()
        print("Server is starting...")
        s.bind(ADDR)
        print(f"Server is hosting on {IP}:{PORT}")
        s.listen()
        print("Waiting for connected...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                prosCode = recvMsg(conn)
                if prosCode == '0':
                    print("Client disconnected!")
                    break
                elif prosCode == '1': checkLogin(conn, dataServer)
                elif prosCode == '2': addAccount(conn, dataServer)
        s.close()

main()