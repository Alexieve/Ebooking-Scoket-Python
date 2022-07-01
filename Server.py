import socket
import json
import os
import datetime
import time

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

class _booked:
    def __init__(self, user, checkin, checkout):
        self.user = user
        self.checkin = checkin
        self.checkout = checkout
class rooms:
    class singleRoom:
        def __init__(self, price, description, empty, notEmpty, booked):
            self.price = price
            self.description = description
            self.empty = empty
            self.notEmpty = notEmpty
            self.listBooked = [booked]
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

def checkExistHotel(dataserver,hotelName):
    for i in dataserver.listHotels:
        if (i.name == hotelName):
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
            print("Account exist!")
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
def loadUsersData(dataServer):
    print("Loading users data...")
    with open("usersdata.json", "r") as readFile:
        dataStr = json.load(readFile)
        for i in dataStr['users']:
            dataServer.listUsers.append(users(i['username'], i['password'], i['cardID']))
    print("Loading complete!")
def loadHotelsData(dataServer):
    print("Loading hotels data...")
    with open("hotelsdata.json", "r") as readFile:
        dataStr = json.load(readFile)
        for i in dataStr['hotels']:
            dataServer.listHotels.append(hotels(i['name'], i['ID'], i['rooms']))
    print("Loading complete!")
def showUsersData(dataServer):
    print("Showing users data...")
    for i in dataServer.listUsers:
        print(i.username)
        print(i.password)
        print(i.cardID)
    print("Loading complete!")
def showHotelsData(dataServer):
    print("Showing hotels data...")
    for i in dataServer.listHotels:
        print(i.rooms['single']['price'])
    print("Loading complete!")

def sendHotelsInfo(s,dataServer,hotelName,dateArrive,DateLeft):
    temp = 'single'
    ok= 1
    for i in dataServer.listHotels:
        if(i.name == hotelName):
            sendMsg(s,hotelName)
            while True:
                dateBooked = i.rooms[temp]['listBooked']['checkin']
                dateBookedLeft = i.rooms[temp]['listBooked']['checkout']
                if(DateLeft < dateBooked or dateArrive > dateBookedLeft or int(i.rooms[temp]['empty']) > 0):
                    sendMsg(s,i.rooms[temp]['description'])
                    sendMsg(s,i.rooms[temp]['price'])
                else sendMsg(s,'NONE_INFO')
                if(ok ==1):
                    temp='double'
                    ok = 2
                    continue
                if(ok ==2):
                    temp = 'family'
                    ok = 3
                    continue
                if(ok == 3):break

def findHotel(s,dataServer):
    print("Listening hotel's request from client")
    hotelName = recvMsg(s)
    showRecvData(hotelName)
    exist = checkExistHotel(dataServer, hotelName)
    if exist == "False":
        print("No such hotel match the search")
        sendMsg(s,'0')
    sendMsg(s,'1')
    dateArrive = recvMsg(s)
    dateLeft = recvMsg(s)
    showRecvData(dateArrive,dateLeft)
    sendHotelsInfo(s, dataServer,hotelName,dateArrive,dateLeft)


def bookingHotel(s,dataServer):
    print("Listening hotel to book from client")
    hotelName = recvMsg(s)
    showRecvData(hotelName)
    exist = checkExistHotel(dataServer, hotelName)
    if exist == True:
        print("No such hotel match the search")
        sendMsg(s, '0')
    sendMsg(s, '1')



##### MAIN #####
def main():
    dataServer = dataBase
    loadUsersData(dataServer)
    loadHotelsData(dataServer)
    # showHotelsData(dataServer)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        cls()
        print("Server is starting...")
        s.bind(ADDR)
        print(f"Server is hosting on {IP}:{PORT}")
        s.listen()
        print("Waiting for connected...")
        name='fivestar'
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
                elif prosCode == '3': findHotel(conn,dataServer)
                elif prosCode == '4': bookingHotel(conn,dataServer)
        s.close()

main()