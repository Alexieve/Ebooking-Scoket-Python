from serverLib import *
#1
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
#2
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
#3
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
    availableTime = checkTime(dateArrive, dateLeft)
    if not availableTime:
        print("The time is not valid!")
        sendMsg(s, "The time is not valid!")
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
        sendMsg(s, "There are no available room now!")
    recvMsg(s)
#4
def bookingHotel(s, serverData):
    print(f"Listening hotel to book from client {s.getpeername()}...")
    hotelName = recvMsg(s)
    sendMsg(s, "ok")
    roomType = recvMsg(s)
    sendMsg(s, "ok")
    sendRoomsInfo(s, serverData, hotelName, roomType)
    print("Booking process is done")
#5
def showNextHotel(s, serverData):
    index = int(recvMsg(s))
    sendMsg(s, "ok")
    while index < 0:
        index += len(serverData[1]['hotels'])
    index = index % len(serverData[1]['hotels'])
    sendHotelsInfo(s, serverData, index)
#6
def addToCart(s, serverData, guest):
    data = json.loads(recvMsg(s))
    sendMsg(s, "ok")
    hotelIndex = findHotelIndex(serverData, data[0])
    hotelData = serverData[1]['hotels'][hotelIndex]
    check = checkEmpty(hotelData, data[1], data[2], data[3])
    if not check:
        print("Not available now!")
        sendMsg(s, "No room available now!")
        recvMsg(s)
    else:
        print("Available room!")
        sendMsg(s, "Add to cart success!")
        recvMsg(s)
        price = hotelData['rooms'][data[1]]['price']
        order = ordered("", data[0], data[1], price, data[2], data[3], "00:00:00", data[4])
        addingUserCart(order, guest, serverData)
#7
def showCart(s, serverData, guest):
    index = int(recvMsg(s))
    sendMsg(s, "ok")
    indexUser = getUserIndex(serverData, guest)
    userCartData = serverData[0]['users'][indexUser]['cart']
    if len(userCartData) == 0:
        sendMsg(s, json.dumps("None"))
        recvMsg(s)
        return
    while index < 0:
        index += len(userCartData)
    index = index % len(userCartData)
    cartData = json.dumps(userCartData[index])
    sendMsg(s, cartData)
    recvMsg(s)
    hotelIndex = findHotelIndex(serverData, userCartData[index]['hotelname'])
    hotelImage = serverData[1]['hotels'][hotelIndex]['image']
    roomImage = serverData[1]['hotels'][hotelIndex]['rooms'][userCartData[index]['roomtype']]['image']
    sendMsg(s, json.dumps([hotelImage, roomImage]))
    recvMsg(s)
    sendMsg(s, json.dumps([str(index + 1), str(len(userCartData))]))
    recvMsg(s)
#8
def editCart(s, serverData, guest):
    index = int(recvMsg(s))
    sendMsg(s, "ok")
    indexUser = getUserIndex(serverData, guest)
    userCartData = serverData[0]['users'][indexUser]['cart']
    if len(userCartData) == 0:
        sendMsg(s, "False")
        recvMsg(s)
        return
    sendMsg(s, "True")
    recvMsg(s)
    while index < 0:
        index += len(userCartData)
    index = index % len(userCartData)
    cartData = json.loads(recvMsg(s))
    sendMsg(s, "ok")
    availableTime = checkTime(cartData[0], cartData[1])
    if not availableTime:
        print("The time is not valid!")
        sendMsg(s, "The time is not valid!")
        recvMsg(s)
        return
    sendMsg(s, "True")
    recvMsg(s)
    userCartData[index]['checkin'] = cartData[0]
    userCartData[index]['checkout'] = cartData[1]
    userCartData[index]['Note'] = cartData[2]
    saveUsersData(serverData[0])
#9
def showOrdered(s, serverData, guest):
    index = int(recvMsg(s))
    sendMsg(s, "ok")
    indexUser = getUserIndex(serverData, guest)
    userOrderData = serverData[0]['users'][indexUser]['listBooked']

    if len(userOrderData) == 0:
        sendMsg(s, json.dumps("None"))
        recvMsg(s)
        return
    while index < 0:
        index += len(userOrderData)
    index = index % len(userOrderData)
    OrderData = json.dumps(userOrderData[index])
    sendMsg(s, OrderData)
    recvMsg(s)
    hotelIndex = findHotelIndex(serverData, userOrderData[index]['hotelname'])
    hotelImage = serverData[1]['hotels'][hotelIndex]['image']
    roomImage = serverData[1]['hotels'][hotelIndex]['rooms'][userOrderData[index]['roomtype']]['image']
    sendMsg(s, json.dumps([hotelImage, roomImage]))
    recvMsg(s)
    sendMsg(s, json.dumps([str(index + 1), str(len(userOrderData))]))
    recvMsg(s)
#10
def deleteCartRoom(s, serverData, guest):
    index = int(recvMsg(s))
    sendMsg(s, "ok")
    indexUser = getUserIndex(serverData, guest)
    userCartData = serverData[0]['users'][indexUser]['cart']
    if len(userCartData) == 0:
        sendMsg(s, "None")
        recvMsg(s)
        return
    sendMsg(s, "True")
    recvMsg(s)
    while index < 0:
        index += len(userCartData)
    index = index % len(userCartData)
    del userCartData[index]
    saveUsersData(serverData[0])
    print("Remove complete!")
#11
def deleteOrderedRoom(s, serverData, guest):
    index = int(recvMsg(s))
    sendMsg(s, "ok")
    indexGuest = 0
    for i in serverData[0]['users']:
        if i['username'] == guest:
            break
        indexGuest += 1
    userOrderedData = serverData[0]['users'][indexGuest]['listBooked']
    if len(userOrderedData) == 0:
        sendMsg(s, "None")
        recvMsg(s)
        return
    sendMsg(s, "True")
    recvMsg(s)

    while index < 0:
        index += len(userOrderedData)
    index = index % len(userOrderedData)
    timeBooked = datetime.strptime(userOrderedData[index]['timeBooked'], '%Y-%m-%d %H:%M:%S')
    timeNow = (datetime.now() - timedelta(hours=24)).replace(microsecond=0)
    if timeNow > timeBooked:
        sendMsg(s, "False")
        recvMsg(s)
        return
    sendMsg(s, "True")
    recvMsg(s)

    idRoom = userOrderedData[index]['id']
    roomType = 'single'
    if idRoom[1] == '1':
        roomType = 'single'
    elif idRoom[1] == '2':
        roomType = 'couple'
    elif idRoom[1] == '3':
        roomType = 'family'
    listBooked = serverData[1]['hotels'][int(idRoom[0]) - 1]['rooms'][roomType]['listBooked']
    indexRoom = 0
    for i in listBooked:
        if i['id'] == idRoom:
            break
        indexRoom += 1
    del serverData[1]['hotels'][int(idRoom[0]) - 1]['rooms'][roomType]['listBooked'][indexRoom]
    Empty = int(serverData[1]['hotels'][int(idRoom[0]) - 1]['rooms'][roomType]['empty']) + 1
    Booked = int(serverData[1]['hotels'][int(idRoom[0]) - 1]['rooms'][roomType]['empty']) - 1
    serverData[1]['hotels'][int(idRoom[0]) - 1]['rooms'][roomType]['empty'] = str(Empty)
    serverData[1]['hotels'][int(idRoom[0]) - 1]['rooms'][roomType]['booked'] = str(Booked)
    saveHotelsData(serverData[1])

    del userOrderedData[index]
    saveUsersData(serverData[0])
    print("Remove complete!")
#12
def checkPayment(s, serverData, guest):
    indexUser = getUserIndex(serverData, guest)
    userCartData = serverData[0]['users'][indexUser]['cart']
    roomCount = len(userCartData)
    if roomCount == 0:
        sendMsg(s, "None")
        recvMsg(s)
        return
    sendMsg(s, "True")
    recvMsg(s)

    checkRemove = "False"
    indexCart = 0
    totalPrice = 0
    for i in userCartData:
        check = removeNotAvailableOrder(serverData, i)
        if not check:
            checkRemove = "Some orders in the cart have been removed because there are no available rooms"
            roomCount -= 1
            del serverData[0]['users'][indexUser]['cart'][indexCart]
        else:
            indexCart += 1
            totalPrice += int(i['price'])
    saveUsersData(serverData[0])

    sendMsg(s, json.dumps([guest, roomCount, totalPrice, checkRemove]))
    recvMsg(s)
    print("Checking complete!")
#13
def goPayment(s, serverData, guest):
    cardID = recvMsg(s)
    sendMsg(s, "ok")

    check = cardIDChecking(serverData, cardID, guest)
    if not check:
        sendMsg(s, "Wrong Card ID!")
        recvMsg(s)
        return

    check = sendCartTolistBooked(serverData, guest)
    if not check:
        sendMsg(s, "Payment complete!")
        recvMsg(s)
    else:
        sendMsg(s, "Some orders in the cart have been removed because there are no available rooms")
        recvMsg(s)