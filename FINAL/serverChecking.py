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

def checkExistHotel(serverData, hotelName):
    for i in serverData[1]['hotels']:
        if (i['name'] == hotelName):
            return True
    return False

def checkTime(dateArrive, dateLeft):
    dateArrive = datetime.strptime(dateArrive, '%Y-%m-%d').date()
    dateLeft = datetime.strptime(dateLeft, '%Y-%m-%d').date()
    if dateArrive > dateLeft:
        return False
    return True

def checkEmpty(hotelData, roomType, dateArrive, dateLeft):
    empty = False
    dateArrive = datetime.strptime(dateArrive, '%Y-%m-%d').date()
    dateLeft = datetime.strptime(dateLeft, '%Y-%m-%d').date()
    if dateArrive > dateLeft:
        return False
    haveBooked = False
    for i in hotelData['rooms'][roomType]['listBooked']:
        haveBooked = True
        dateBooked = datetime.strptime(i['checkin'], '%Y-%m-%d').date()
        dateBookedLeft = datetime.strptime(i['checkout'], '%Y-%m-%d').date()
        if (dateLeft < dateBooked or dateArrive > dateBookedLeft) and int(hotelData['rooms'][roomType]['empty']) > 0:
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

def removeNotAvailableOrder(serverData, cartData):
    hotelIndex = findHotelIndex(serverData, cartData['hotelname'])
    hotelData = serverData[1]['hotels'][hotelIndex]
    check = checkEmpty(hotelData, cartData['roomtype'], cartData['checkin'], cartData['checkout'])
    return check