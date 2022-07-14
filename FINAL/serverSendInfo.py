from serverLib import *

def sendHotelsInfo(s, serverData, index):
    sendMsg(s, json.dumps(serverData[1]['hotels'][index]))
    recvMsg(s)
    sendMsg(s, json.dumps([str(index + 1), str(len(serverData[1]['hotels']))]))
    recvMsg(s)
    print(f"Sending hotels information for client {s.getpeername()} complete!")

def sendRoomsInfo(s, serverData, hotel, roomType):
    hotelIndex = findHotelIndex(serverData, hotel)
    room = json.dumps(serverData[1]['hotels'][hotelIndex]['rooms'][roomType])
    sendMsg(s, room)
    recvMsg(s)
    print(f"Sending room information for client {s.getpeername()} complete!")

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