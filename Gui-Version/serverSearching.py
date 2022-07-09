from serverLib import *

def showNextHotel(s, serverData):
    hotelName = recvMsg(s)
    sendMsg(s, "ok")
    check = recvMsg(s)
    sendMsg(s, "ok")
    index = 0
    for i in serverData[1]['hotels']:
        if i['name'] == hotelName:
            break
        index += 1
    if check == "prev":
        index -= 1
    else:
        index += 1
    if index == 3:
        index = 0
    elif index == -1:
        index = 2
    sendHotelsInfo(s, serverData, index)

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
    sendMsg(s, "True")
    recvMsg(s)

    index = 0
    for i in serverData[1]['hotels']:
        if i['name'] == searchHotel:
            sendHotelsInfo(s, serverData, index)
            if (checkEmpty(i, "single", dateArrive, dateLeft)
                and checkEmpty(i, "couple", dateArrive, dateLeft)
                and checkEmpty(i, "family", dateArrive, dateLeft)):
                sendMsg(s, "True")
            else: sendMsg("There are no available room now!")
            recvMsg(s)
            return
        index += 1

