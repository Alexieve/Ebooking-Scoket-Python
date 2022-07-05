from serverLib import *

def addAccount(s, serverData):
    print("Adding account to database...")
    while True:
        username = str(recvMsg(s))
        showRecvData(username)
        exits = checkExistAccount(serverData, username)
        print("!@#!@#!@")
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
        addingUserData(serverData, username, password, cardID)
        return

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

def checkLogin(s, serverData):
    print(f"Checking login of client {s.getpeername()}...")
    username = recvMsg(s)
    password = recvMsg(s)
    fromClient(s)
    showRecvData(username, password)
    for i in serverData[0]['users']:
        if (username == i['username'] and password == i['password']):
            sendMsg(s, "True")
            print("Checking complete!")
            return username
    sendMsg(s, "False")
    print("Checking complete!")

def checkEmpty(hotelName, roomType, dateArrive, dateLeft, serverData):
    for i in serverData[1]['hotels']:
        if(i['name'] == hotelName):
            while True:
                empty = False
                haveBooked = False
                for j in i['rooms'][roomType]['listBooked']:
                    haveBooked = True
                    dateBooked = datetime.datetime.strptime(j['checkin'], "%d/%m/%y")
                    dateBookedLeft = datetime.datetime.strptime(j['checkout'], "%d/%m/%y")
                    if(dateLeft < dateBooked or dateArrive > dateBookedLeft or int(i['rooms'][roomType]['empty']) > 0):
                        return True
                if not empty and haveBooked:
                    return False
                if not haveBooked:
                    return True
            break

def cardIDChecking(serverData, cardID, guest):
    for i in serverData[0]['users']:
        if i['username'] == guest:
            if i['cardID'] == cardID: return True
            else: return False