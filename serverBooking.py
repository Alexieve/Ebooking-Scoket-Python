from serverLib import *

def idGenerator(name, type, serverData):
    id = 0
    for i in serverData[1]['hotels']:
        id += 1
        if i['name'] == name:break
    id *= 100
    if type == 'single': id += 10
    elif type == 'couple': id += 20
    elif type == 'family': id += 30
    fid = str(id + int(i['rooms'][type]['booked']) + 1)
    return fid

def dateToStr(str): ## :>>>>>>>
    day = str[8:10]
    month = str[5:7]
    year = str[2:4]
    date = day + '/' + month + '/' + year
    return date

def paymentCount(name, type, serverData):
    for i in serverData[1]['hotels']:
        if(i['name'] == name):
            price = int(i['rooms'][type]['price'])
            break
    return price

def bookingRooms(s, hotelName, serverData, guest):
    while True:
        roomType = recvMsg(s)
        fromClient(s)
        showRecvData(roomType)
        sendMsg(s, "ok")
        dateArrive = datetime.datetime.strptime(recvMsg(s), "%d/%m/%y")
        dateLeft = datetime.datetime.strptime(recvMsg(s), "%d/%m/%y")
        fromClient(s)
        showRecvData(dateArrive,dateLeft)
        empty = checkEmpty(hotelName, roomType, dateArrive, dateLeft, serverData)
        if not empty:
            sendMsg(s,'False')
            continue
        sendMsg(s, 'True')
        note = recvMsg(s)
        fromClient(s)
        showRecvData(note)
        print(note)
        break
    arriveTmp = str(dateArrive) ##không hỗ trợ dateTime nên phải biến qua string
    leftTmp = str(dateLeft)
    arrive = dateToStr(arriveTmp)
    left = dateToStr(leftTmp)
    id = idGenerator(hotelName, roomType, serverData)
    ###Saving process
    with open("hotelsdata.json") as file:
        data = json.load(file)
        hotel = data['hotels']
        for i in hotel:
            if i['name'] == hotelName:
                tmpRoom = i['rooms'][roomType]
                bookedData = booked(guest, id, arrive, left, note)
                bookedDataJson = {'username': bookedData.user, 'id': bookedData.id, 'checkin': bookedData.checkin, 'checkout': bookedData.checkout, 'Note': bookedData.Note}
                tmpRoom['listBooked'].append(bookedDataJson)
    serverData[1] = data
    saveHotelsData(serverData[1])
    print("Adding hotel_listbooked complete!")
    ###Saving user data process
    saveUserBooked(s, id, guest, serverData)
    price = paymentCount(hotelName,roomType, serverData)
    return price

def bookingHotel(s, serverData, guest):
    print(f"Listening hotel to book from client {s.getpeername()}...")
    while True:
        hotelName = recvMsg(s)
        fromClient(s)
        showRecvData(hotelName)
        exist = checkExistHotel(serverData, hotelName)
        if exist == False:
            print("No such hotel match the search")
            sendMsg(s, 'False')
            continue
        break
    print("Valid hotel to book")
    sendMsg(s, "True")
    pay = 0
    while True:
        pay += bookingRooms(s,hotelName,serverData,guest)
        if recvMsg(s) == 'continue':
            continue
        break
    sendMsg(s, str(pay)) ##
    while True:
        cardID = recvMsg(s)
        rightID = cardIDChecking(serverData,cardID,guest)
        if rightID == False :
            sendMsg(s, 'again')
            continue
        sendMsg(s, 'ok')
        break
    print("Booking process is done")