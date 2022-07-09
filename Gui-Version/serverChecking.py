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
    hotel = json.dumps(serverData[1]['hotels'][index])
    sendMsg(s, hotel)
    recvMsg(s)
    print(f"Sending hotels information for client {s.getpeername()} complete!")

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
            sendHotelsInfo(s, serverData, 0)
            print("Checking complete!")
            return accountData[0]
    sendMsg(s, "Wrong username or password!")
    print("Checking complete!")

def checkEmpty(hotelData, roomType, dateArrive, dateLeft):
    empty = False
    dateArrive = datetime.strptime(dateArrive, '%Y-%m-%d').date()
    dateLeft = datetime.strptime(dateLeft, '%Y-%m-%d').date()
    haveBooked = False
    for i in hotelData['rooms'][roomType]['listBooked']:
        haveBooked = True
        dateBooked = datetime.strptime(i['checkin'], '%Y-%m-%d').date()
        dateBookedLeft = datetime.strptime(i['checkout'], '%Y-%m-%d').date()
        if(dateLeft < dateBooked or dateArrive > dateBookedLeft or int(i['rooms'][roomType]['empty']) > 0):
            return True
    if not empty and haveBooked:
        return False
    if not haveBooked:
        return True

def cardIDChecking(serverData, cardID, guest):
    for i in serverData[0]['users']:
        if i['username'] == guest:
            if i['cardID'] == cardID:
                return True
            else:
                return False