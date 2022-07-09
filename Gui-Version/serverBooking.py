from serverLib import *

def idGenerator(name, type, serverData):
    id = 1
    for i in serverData[1]['hotels']:
        if i['name'] == name:
            hotel = i
            break
        id += 1
    id *= 100

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

def checkPayment(s, serverData, guest):
    for i in serverData[0]['users']:
        if i['username'] == guest:
            userCartData = i['cart']
            break
    roomCount = len(userCartData)
    if roomCount == 0:
        sendMsg(s, "None")
        recvMsg(s)
        return
    sendMsg(s, "True")
    recvMsg(s)

    totalPrice = 0
    for i in userCartData:
        totalPrice += int(i['price'])
    sendMsg(s, json.dumps([guest, roomCount, totalPrice]))
    recvMsg(s)
    print("Checking complete!")

def sendCartTolistBooked(serverData, guest):
    userIndex = 0
    for i in serverData[0]['users']:
        if i['username'] == guest:
            cartData = i['cart']
            break
        userIndex += 1

    timeBooked = str(datetime.now().replace(microsecond=0))
    for i in cartData:
        id = idGenerator(i['hotelname'], i['roomtype'], serverData)

        order = ordered(id, i['hotelname'], i['roomtype'], i['price'],
                        i['checkin'], i['checkout'], timeBooked, i['Note'])
        addingUserBooked(order, guest, serverData)
    serverData[0]['users'][userIndex]['cart'].clear()
    saveUsersData(serverData[0])

def goPayment(s, serverData, guest):
    cardID = recvMsg(s)
    sendMsg(s, "ok")
    check = cardIDChecking(serverData, cardID, guest)
    if not check:
        sendMsg(s, "Wrong Card ID!")
        recvMsg(s)
        return

    sendCartTolistBooked(serverData, guest)
    sendMsg(s, "Payment complete!")
    recvMsg(s)

def deleteOrderedRoom(s, serverData, guest):
    index = int(recvMsg(s))
    sendMsg(s, "ok")
    for i in serverData[0]['users']:
        if i['username'] == guest:
            userOrderedData = i['listBooked']
            break
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
    for i in serverData[0]['users']:
        if i['username'] == guest:
            userCartData = i['cart']
            break
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
    for i in serverData[0]['users']:
        if i['username'] == guest:
            userOrderData = i['listBooked']
            break
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

def editCart(s, serverData, guest):
    index = int(recvMsg(s))
    sendMsg(s, "ok")
    for i in serverData[0]['users']:
        if i['username'] == guest:
            userCartData = i['cart']
            break
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
    for i in serverData[0]['users']:
        if i['username'] == guest:
            userCartData = i['cart']
            break
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