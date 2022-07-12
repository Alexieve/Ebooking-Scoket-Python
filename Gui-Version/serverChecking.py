import json

from serverLib import *

def checkValidUsername(username):
    if len(username) < 5:
        return False
    for i in username:
        if ('a' <= i and i <= 'z') or ('0' <= i and i <= '9'):
            continue
        else:
            return False
    return True

def checkValidPassword(password):
    if len(password) < 3:
        return False
    return True

def checkValidCardID(cardID):
    if len(cardID) != 10:
        return False
    for i in cardID:
        if i < '0' or '9' < i:
            return False
    return True

def checkExistAccount(serverData, username):
    for i in serverData[0]['users']:
        if (i['username'] == username):
            return False
    return True

def addAccount(s, serverData):
    print("Adding account to database...")
    accountData = json.loads(recvMsg(s))
    sendMsg(s, "ok")
    username = accountData[0]
    password = accountData[1]
    confirm = accountData[2]
    cardID = accountData[3]
    showRecvData(username, password, confirm, cardID)
    if password != confirm: exits = "Confirm password does not match"
    elif not checkValidUsername(username): exits = "Invalid username, the minimum length is 5 (a-z, 0-9)"
    elif not checkValidPassword(password): exits = "Invalid password, the minimum length is 3"
    elif not checkValidCardID(cardID): exits = "Invalid card ID, the length is 10 (0-9)"
    elif not checkExistAccount(serverData, username): exits = "The username has already taken!"
    else: exits = "Sign-up success!"
    sendMsg(s, exits)
    if exits != "Sign-up success!":
        print("Not valid!")
        return
    print("Valid account!")
    addingUserData(serverData, username, password, cardID)

def checkExistHotel(serverData, hotelName):
    for i in serverData[1]['hotels']:
        if (i['name'] == hotelName):
            return True
    return False

def sendHotelsInfo(s, serverData, index):
    sendMsg(s, json.dumps(serverData[1]['hotels'][index]))
    recvMsg(s)
    sendMsg(s, json.dumps([str(index + 1), str(len(serverData[1]['hotels']))]))
    recvMsg(s)
    print(f"Sending hotels information for client {s.getpeername()} complete!")

def showNextHotel(s, serverData):
    index = int(recvMsg(s))
    sendMsg(s, "ok")
    while index < 0:
        index += len(serverData[1]['hotels'])
    index = index % len(serverData[1]['hotels'])
    sendHotelsInfo(s, serverData, index)

def findHotelIndex(serverData, hotelName):
    check = False
    index = 0
    for i in serverData[1]['hotels']:
        if i['name'] == hotelName:
            check = True
            break
        index += 1
    if check:
        return index
    else:
        return False

def findHotel(s, serverData):
    print(f"Listening hotel's request from client {s.getpeername()}...")
    data = json.loads(recvMsg(s))
    sendMsg(s, "ok")
    searchHotel = data[0]
    dateArrive = data[1]
    dateLeft = data[2]
    showRecvData(searchHotel, dateArrive, dateLeft)

    exitsHotel = checkExistHotel(serverData, searchHotel)
    if not exitsHotel:
        print("Hotel not exits!")
        sendMsg(s, "Hotel does not exits!")
        recvMsg(s)
        return
    print("Valid hotels")
    hotelIndex = findHotelIndex(serverData, searchHotel)
    sendMsg(s, str(hotelIndex))
    recvMsg(s)
    recvMsg(s)
    sendMsg(s, "ok")

    sendHotelsInfo(s, serverData, hotelIndex)
    if (checkEmpty(serverData[1]['hotels'][hotelIndex], "single", dateArrive, dateLeft)
        and checkEmpty(serverData[1]['hotels'][hotelIndex], "couple", dateArrive, dateLeft)
        and checkEmpty(serverData[1]['hotels'][hotelIndex], "family", dateArrive, dateLeft)):
        sendMsg(s, "True")
    else:
        sendMsg("There are no available room now!")
    recvMsg(s)

def checkLogin(s, serverData):
    print(f"Checking login of client {s.getpeername()}...")
    accountData = json.loads(recvMsg(s))
    sendMsg(s, "ok")
    fromClient(s)
    showRecvData(accountData[0], accountData[1])
    for i in serverData[0]['users']:
        if (accountData[0] == i['username'] and accountData[1] == i['password']):
            sendMsg(s, "Login success!")
            recvMsg(s)
            sendMsg(s, accountData[0])
            recvMsg(s)
            showNextHotel(s, serverData)
            print("Checking complete!")
            return accountData[0]
    sendMsg(s, "Wrong username or password!")
    print("Checking complete!")

def cardIDChecking(serverData, cardID, guest):
    for i in serverData[0]['users']:
        if i['username'] == guest:
            if i['cardID'] == cardID:
                return True
            else:
                return False