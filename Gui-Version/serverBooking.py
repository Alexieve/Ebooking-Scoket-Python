from serverLib import *

def idGenerator(name, type, serverData):
    id = 1
    hotel = serverData[1]['hotels'][0]
    for i in serverData[1]['hotels']:
        if i['name'] == name:
            hotel = i
            break
        id += 1
    id *= 100

    room = hotel['rooms']['single']
    if type == 'single':
        room = hotel['rooms']['single']
        id += 10
    elif type == 'couple':
        room = hotel['rooms']['couple']
        id += 20
    elif type == 'family':
        room = hotel['rooms']['family']
        id += 30

    idList = []
    for i in room['listBooked']:
        idList.append(int(i['id'][2]))
    idList.sort()
    idRoom = 1
    indexList = 0
    while indexList < len(idList):
        if idRoom == idList[indexList]:
            idRoom += 1
            indexList += 1
        else:
            break

    fid = str(id + idRoom)
    return fid

def removeNotAvailableOrder(serverData, cartData):
    hotelIndex = findHotelIndex(serverData, cartData['hotelname'])
    hotelData = serverData[1]['hotels'][hotelIndex]
    check = checkEmpty(hotelData, cartData['roomtype'], cartData['checkin'], cartData['checkout'])
    return check

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

def sendCartTolistBooked(serverData, guest):
    indexUser = getUserIndex(serverData, guest)
    cartData = serverData[0]['users'][indexUser]['cart']

    timeBooked = str(datetime.now().replace(microsecond=0))
    checkRemove = False
    userData = serverData[0]
    hotelData = serverData[1]
    index = 0
    for i in cartData:
        id = idGenerator(i['hotelname'], i['roomtype'], serverData)
        order = ordered(id, i['hotelname'], i['roomtype'], i['price'],
                        i['checkin'], i['checkout'], timeBooked, i['Note'])
        check = addingUserBooked(userData, hotelData, order, guest)
        if check[0] == False:
            checkRemove = True
            del serverData[0]['users'][indexUser]['cart'][index]
        else:
            userData = check[0]
            hotelData = check[1]
            index += 1
        del userData['users'][indexUser]['cart'][0]

    if not checkRemove:
        serverData[0] = userData
        serverData[1] = hotelData
    saveUsersData(serverData[0])
    saveHotelsData(serverData[1])
    return checkRemove

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
    del listBooked[indexRoom]
    saveHotelsData(serverData[1])

    del userOrderedData[index]
    saveUsersData(serverData[0])
    print("Remove complete!")

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
    userCartData[index]['checkin'] = cartData[0]
    userCartData[index]['checkout'] = cartData[1]
    userCartData[index]['Note'] = cartData[2]
    saveUsersData(serverData[0])

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

def addToCart(s, serverData, guest):
    data = json.loads(recvMsg(s))
    sendMsg(s, "ok")
    hotelIndex = findHotelIndex(serverData, data[0])
    hotelData = serverData[1]['hotels'][hotelIndex]
    check = checkEmpty(hotelData, data[1], data[2], data[3])
    if check:
        print("Available room!")
        sendMsg(s, "Add to cart success!")
        recvMsg(s)
        price = hotelData['rooms'][data[1]]['price']
        order = ordered("", data[0], data[1], price, data[2], data[3], "00:00:00", data[4])
        addingUserCart(order, guest, serverData)
    else:
        print("Not available now!")
        sendMsg(s, "No room available now!")
        recvMsg(s)

def sendRoomsInfo(s, serverData, hotel, roomType):
    hotelIndex = findHotelIndex(serverData, hotel)
    room = json.dumps(serverData[1]['hotels'][hotelIndex]['rooms'][roomType])
    sendMsg(s, room)
    recvMsg(s)
    print(f"Sending room information for client {s.getpeername()} complete!")

def bookingHotel(s, serverData):
    print(f"Listening hotel to book from client {s.getpeername()}...")
    hotelName = recvMsg(s)
    sendMsg(s, "ok")
    roomType = recvMsg(s)
    sendMsg(s, "ok")
    sendRoomsInfo(s, serverData, hotelName, roomType)
    print("Booking process is done")