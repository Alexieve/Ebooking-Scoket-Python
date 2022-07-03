import socket
import json
import os
import datetime

IP = "127.0.0.1"
PORT = 1234
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

###### Processing code #####
# 0 Exit
# 1 Check login
# 2 Add account
# 3 Searching Hotels
# 4 Booking Hotels

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
        s.sendall(bytes(i, FORMAT))

def recvMsg(s):
    return s.recv(SIZE).decode(FORMAT)

def checkExistAccount(serverData, username):
    for i in serverData[0]['users']:
        if (i['username'] == username):
            return True
    return False

def checkExistHotel(serverData, hotelName):
    for i in serverData[1]['hotels']:
        if (i['name'] == hotelName):
            return True
    return False

def encoderUser(user):
    if isinstance(user, users):
        return {'username': user.username, 'password': user.password, 'cardID': user.cardID}
    raise TypeError(f'Object {user} is not of type users.')

### MAIN FUNCTIONS ###
def addAccount(s, serverData):
    print("Adding account to database...")
    while True:
        username = str(recvMsg(s))
        showRecvData(username)
        exits = checkExistAccount(serverData, username)
        if (exits):
            print("Account exist!")
            sendMsg(s, "True")
            continue
        else:
            print("Valid account!")
            sendMsg(s, "False")
        password = recvMsg(s)
        cardID = recvMsg(s)
        showRecvData(password, cardID)
        with open("usersdata.json") as file:
            data = json.load(file)
            tmp = data["users"]
            user = users(username, password, cardID)
            usertmp = {'username': user.username, 'password': user.password, 'cardID': user.cardID}
            tmp.append(usertmp)
        serverData[0] = data
        saveUsersData(serverData[0])
        print("Adding account complete!")
        return

def checkLogin(s, serverData):
    print("Checking login of client...")
    username = recvMsg(s)
    password = recvMsg(s)
    showRecvData(username, password)
    for i in serverData[0]['users']:
        if (username == i['username'] and password == i['password']):
            sendMsg(s, "True")
            print("Checking complete!")
            return
    sendMsg(s, "False")
    print("Checking complete!")

def saveUsersData(usersData):
    print("Saving users data...")
    with open("usersdata.json", 'w') as writeFile:
        json.dump(usersData, writeFile, indent=4)
    print("Saving complete!")

def saveHotelsData(hotelsData):
    print("Saving hotels data...")
    with open("hotelsdata.json", 'w') as writeFile:
        json.dump(hotelsData, writeFile, indent=4)
    print("Saving complete!")

def loadUsersData():
    print("Loading users data...")
    with open("usersdata.json", "r") as readFile:
        usersData = json.load(readFile)
    print("Loading complete!")
    return usersData

def loadHotelsData():
    print("Loading hotels data...")
    with open("hotelsdata.json", "r") as readFile:
        hotelsData = json.load(readFile)
    print("Loading complete!")
    return hotelsData

def sendHotelsInfo(s,serverData, hotelName):
    dateArrive = datetime.datetime.strptime(recvMsg(s), "%d/%m/%y")
    dateLeft = datetime.datetime.strptime(recvMsg(s), "%d/%m/%y")
    showRecvData(dateArrive, dateLeft)
    temp = 'single'
    ok = 1
    for i in serverData[1]['hotels']:
        if(i['name'] == hotelName):
            while True:
                empty = False
                haveBooked = False
                for j in i['rooms'][temp]['listBooked']:
                    haveBooked = True
                    dateBooked = datetime.datetime.strptime(j['checkin'], "%d/%m/%y")
                    dateBookedLeft = datetime.datetime.strptime(j['checkout'], "%d/%m/%y")
                    if(dateLeft < dateBooked or dateArrive > dateBookedLeft or int(i['rooms'][temp]['empty']) > 0):
                        sendMsg(s, i['rooms'][temp]['description'])
                        recvMsg(s)
                        sendMsg(s, i['rooms'][temp]['price'])
                        empty = True
                        break
                if not empty and haveBooked:
                    sendMsg(s, "NONE_INFO")
                    recvMsg(s)
                    sendMsg(s, "NONE_INFO")
                if not haveBooked:
                    sendMsg(s, i['rooms'][temp]['description'])
                    recvMsg(s)
                    sendMsg(s, i['rooms'][temp]['price'])
                if ok == 1:
                    temp = "couple"
                    ok = 2
                elif ok == 2:
                    temp = "family"
                    ok = 3
                elif ok == 3: break
            break
    print("Sending hotels information complete!")

def findHotel(s,serverData):
    print("Listening hotel's request from client")
    while True:
        hotelName = recvMsg(s)
        showRecvData(hotelName)
        exist = checkExistHotel(serverData, hotelName)
        if exist == False:
            print("No such hotel match the search")
            sendMsg(s, "False")
            continue
        print("Valid hotels")
        sendMsg(s, "True")
        sendHotelsInfo(s, serverData, hotelName)

def bookingHotel(s,serverData):
    print("Listening hotel to book from client")
    hotelName = recvMsg(s)
    showRecvData(hotelName)
    exist = checkExistHotel(serverData, hotelName)
    if exist == True:
        print("No such hotel match the search")
        sendMsg(s, '0')
    sendMsg(s, '1')

##### MAIN #####
def main():
    # serverData = dataBase
    usersData = loadUsersData()
    hotelsData = loadHotelsData()
    serverData = [usersData, hotelsData]
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
                elif prosCode == '1': checkLogin(conn, serverData)
                elif prosCode == '2': addAccount(conn, serverData)
                elif prosCode == '3': findHotel(conn, serverData)
                elif prosCode == '4': bookingHotel(conn, serverData)
        s.close()

main()