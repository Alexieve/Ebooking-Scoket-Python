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

class booked:
    class checkInTime:
        def __init__(self, date, month, year):
            self.date = date
            self.month = month
            self.year = year
    class checkOutTime:
        def __init__(self, date, month, year):
            self.date = date
            self.month = month
            self.year = year

    def __init__(self, user, checkInTime, checkOutTime):
        self.user = user
        self.checkin = checkInTime
        self.checkout = checkOutTime

class rooms:
    class singleRoom:
        def __init__(self, price, description, empty, notEmpty, booked):
            self.price = price
            self.description = description
            self.empty = empty
            self.notEmpty = notEmpty
            self.listBooked = list(booked)
    class coupleRoom:
        def __init__(self, price, description, empty, notEmpty, booked):
            self.price = price
            self.description = description
            self.empty = empty
            self.notEmpty = notEmpty
            self.listBooked = list(booked)
    class familyRoom:
        def __init__(self, price, description, empty, notEmpty, booked):
            self.price = price
            self.description = description
            self.empty = empty
            self.notEmpty = notEmpty
            self.listBooked = list(booked)
    def __init__(self, singleRoom, coupleRoom, familyRoom):
        self.single = list(singleRoom)
        self.couple = list(coupleRoom)
        self.family = list(familyRoom)
class hotels:
    def __init__(self, name, ID, rooms):
        self.name = name
        self.ID = ID
        self.rooms = rooms
class dataBase:
    listUsers = []
    listHotels = []

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
    with open("usersdata.json", "r") as readFile:
        dataStr = json.load(readFile)
        for i in dataStr['users']:
            dataServer.listUsers.append(users(i['username'], i['password'], i['cardID']))
    print("Loading complete!")
def showDatabase(dataServer):
    print("Showing database...")
    for i in dataServer.listUser:
        print(i.username)
        print(i.password)
        print(i.cardID)
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