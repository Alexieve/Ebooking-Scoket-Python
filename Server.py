import socket
import json
import os
import datetime

IP = "127.0.0.1"
PORT = 1234
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

###### Processing code #####
# 0 Exit
# 1 Check login
# 2 Add account
# 3 Searching Hotels
# 4 Booking Hotels

##### CLASS #####
class booked:
    def __init__(self, user, id, checkin, checkout, Note):
        self.user = user
        self.id = id
        self.checkin= checkin
        self.checkout= checkout
        self.Note= Note

class users:
    def __init__(self, username, password, cardID):
        self.username = username
        self.password = password
        self.cardID = cardID
        self.listBooked = []


##### PROCESS FUNCTIONS #####
def cls():
    os.system('cls')

def waitForInput():
    input("Press ENTER to continue...")

def showRecvData(*list):
    print("From client:")
    for i in list:
        print(i)

def sendMsg(s, *listMsg):
    for i in listMsg:
        s.sendall(bytes(i, FORMAT))

def recvMsg(s):
    return s.recv(SIZE).decode(FORMAT)

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

def encoderUser(user):
    if isinstance(user, users):
        return {'username': user.username, 'password': user.password, 'cardID': user.cardID}
    raise TypeError(f'Object {user} is not of type users.')

### MAIN FUNCTIONS ###
def addAccount(s, serverData):
    print("Adding account to database...")
    while True:
        username = str(recvMsg(s))
        showRecvData(username)
        exits = checkExistAccount(serverData, username)
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
        with open("usersdata.json") as file:
            data = json.load(file)
            tmp = data["users"]
            user = users(username, password, cardID)
            usertmp = {'username': user.username, 'password': user.password, 'cardID': user.cardID, 'listBooked': user.listBooked}
            tmp.append(usertmp)
        serverData[0] = data
        saveUsersData(serverData[0])
        print("Adding account complete!")
        return

def checkLogin(s, serverData):
    print("Checking login of client...")
    username = recvMsg(s)
    password = recvMsg(s)
    showRecvData(username, password)
    for i in serverData[0]['users']:
        if (username == i['username'] and password == i['password']):
            sendMsg(s, "True")
            print("Checking complete!")
            return username
    sendMsg(s, "False")
    print("Checking complete!")

def saveUsersData(usersData):
    print("Saving users data...")
    with open("usersdata.json", 'w') as writeFile:
        json.dump(usersData, writeFile, indent=4)
    print("Saving complete!")

def saveHotelsData(hotelsData):
    print("Saving hotels data...")
    with open("hotelsdata.json", 'w') as writeFile:
        json.dump(hotelsData, writeFile, indent=4)
    print("Saving complete!")

def loadUsersData():
    print("Loading users data...")
    with open("usersdata.json", "r") as readFile:
        usersData = json.load(readFile)
    print("Loading complete!")
    return usersData

def loadHotelsData():
    print("Loading hotels data...")
    with open("hotelsdata.json", "r") as readFile:
        hotelsData = json.load(readFile) #à hiểu, để tui xuống đó check phát
        #tui tưởng lỗi bên server chứ, tại tới đó tui thấy server nó bị tắt nên cho dù client gửi gì đâu có được nhỉ ?
    print("Loading complete!")
    return hotelsData

def sendHotelsInfo(s,serverData, hotelName):
    dateArrive = datetime.datetime.strptime(recvMsg(s), "%d/%m/%y")
    dateLeft = datetime.datetime.strptime(recvMsg(s), "%d/%m/%y")
    showRecvData(dateArrive, dateLeft)
    temp = 'single'
    ok = 1
    for i in serverData[1]['hotels']:
        if(i['name'] == hotelName):
            while True:
                empty = False
                haveBooked = False
                for j in i['rooms'][temp]['listBooked']:
                    haveBooked = True ###Có người khác đã đặt
                    dateBooked = datetime.datetime.strptime(j['checkin'], "%d/%m/%y")
                    dateBookedLeft = datetime.datetime.strptime(j['checkout'], "%d/%m/%y")
                    if(dateLeft < dateBooked or dateArrive > dateBookedLeft or int(i['rooms'][temp]['empty']) > 0):
                        sendMsg(s, i['rooms'][temp]['description'])
                        recvMsg(s)
                        sendMsg(s, i['rooms'][temp]['price'])
                        empty = True
                        break
                if not empty and haveBooked:
                    sendMsg(s, "NONE_INFO")
                    recvMsg(s)
                    sendMsg(s, "NONE_INFO")
                if not haveBooked:
                    sendMsg(s, i['rooms'][temp]['description'])
                    recvMsg(s)
                    sendMsg(s, i['rooms'][temp]['price'])
                if ok == 1:
                    temp = "couple"
                    ok = 2
                elif ok == 2:
                    temp = "family"
                    ok = 3
                elif ok == 3: break
            break
    print("Sending hotels information complete!")

def findHotel(s,serverData):
    print("Listening hotel's request from client")
    while True:
        hotelName = recvMsg(s)
        showRecvData(hotelName)
        exist = checkExistHotel(serverData, hotelName)
        if exist == False:
            print("No such hotel match the search")
            sendMsg(s, "False")
            continue
        print("Valid hotel to search")
        sendMsg(s, "True")
        sendHotelsInfo(s, serverData, hotelName)
        break

def checkEmpty(s,hotelName, roomType,dateArrive,dateLeft,serverData):   ###đáng lẽ nên xài hàm này cho searchHotel luôn :<
    for i in serverData[1]['hotels']:
        if(i['name'] == hotelName):
            while True:
                empty = False
                haveBooked = False
                for j in i['rooms'][roomType]['listBooked']:
                    haveBooked = True ###Có người khác đã đặt
                    dateBooked = datetime.datetime.strptime(j['checkin'], "%d/%m/%y")
                    dateBookedLeft = datetime.datetime.strptime(j['checkout'], "%d/%m/%y")
                    if(dateLeft < dateBooked or dateArrive > dateBookedLeft or int(i['rooms'][roomType]['empty']) > 0):
                        return True
                if not empty and haveBooked:
                    return False
                if not haveBooked:
                    return True
            break

def idGenerator(name,type,serverData):
    id = 0
    for i in serverData[1]['hotels']:
        id+=1
        if i['name'] == name:break
    id*=100
    if type == 'single': id+=10
    elif type == 'couple': id+=20
    elif type == 'family': id+=30
    fid = str(id + int(i['rooms'][type]['booked']) +1)
    return fid

def dateToStr(str): ## :>>>>>>>
    day= str[8:10]
    month = str[5:7]
    year = str[2:4]
    date = day + '/' + month+ '/' + year
    return date

def saveUserBooked(s,id,guest,serverData):
    with open("usersdata.json") as file:
        data = json.load(file)
        userss = data["users"]
        for i in userss:
            if i['username'] == guest:
                tmpUser = i['listBooked']
                bookedDataJson = {'id': id}
                tmpUser.append(bookedDataJson)
    serverData[0] = data
    saveUsersData(serverData[0])
    print("Adding user's ID complete!")

def paymentCount(name,type,serverData):
    for i in serverData[1]['hotels']:
        if(i['name'] == name):
            price = int(i['rooms'][type]['price'])
            break
    return price

def bookingRooms(s,hotelName,serverData,guest):
    while True:
        roomType = recvMsg(s)
        showRecvData(roomType)
        sendMsg(s,"ok")
        dateArrive = datetime.datetime.strptime(recvMsg(s), "%d/%m/%y")
        dateLeft = datetime.datetime.strptime(recvMsg(s), "%d/%m/%y")
        showRecvData(dateArrive,dateLeft)
        empty = checkEmpty(s,hotelName,roomType,dateArrive,dateLeft,serverData)
        if not empty:
            sendMsg(s,'False')
            continue
        sendMsg(s,'True')
        note = recvMsg(s)
        showRecvData(note)
        print(note)
        break
    arriveTmp= str(dateArrive) ##không hỗ trợ dateTime nên phải biến qua string
    leftTmp = str(dateLeft)
    arrive = dateToStr(arriveTmp)
    left = dateToStr(leftTmp)
    id = idGenerator(hotelName, roomType, serverData)
    ###Saving process
    with open("hotelsdata.json") as file:
        data = json.load(file)
        hotel = data['hotels']
        for i in hotel:
            if i['name'] == hotelName: #đống này thiếu data nè, truyền lại data đi
                tmpRoom = i['rooms'][roomType]
                bookedData = booked(guest, id, arrive, left, note)
                bookedDataJson = {'username': bookedData.user, 'id': bookedData.id, 'checkin': bookedData.checkin, 'checkout': bookedData.checkout, 'Note': bookedData.Note}
                tmpRoom['listBooked'].append(bookedDataJson)
    serverData[1] = data
    saveHotelsData(serverData[1])
    print("Adding hotel_listbooked complete!")
    ###Saving user data process
    saveUserBooked(s,id,guest,serverData)
    price = paymentCount(hotelName,roomType,serverData)
    return price

def cardIDChecking(serverData,cardID,guest):
    for i in serverData[0]['users']:
        if i['username']== guest:
            if i['cardID'] == cardID:return True
            else: return False

def bookingHotel(s,serverData,guest):
    print("Listening hotel to book from client")
    while True:
        hotelName = recvMsg(s)
        showRecvData(hotelName)
        exist = checkExistHotel(serverData, hotelName)  ###Chack xem Client nhập đúng tên hay không
        if exist == False:
            print("No such hotel match the search")
            sendMsg(s, 'False')
            continue
        break
    print("Valid hotel to book")
    sendMsg(s,"True")
    pay = 0
    while True:
        pay += bookingRooms(s,hotelName,serverData,guest)
        if recvMsg(s) == 'continue':
            continue
        break
    sendMsg(s,str(pay)) ##
    while True:
        cardID = recvMsg(s)
        rightID = cardIDChecking(serverData,cardID,guest)
        if rightID == False :
            sendMsg(s,'again')
            continue
        sendMsg(s,'ok')
        break

    print("Booking process is done")


##### MAIN #####
def main():
    # serverData = dataBase
    usersData = loadUsersData()
    hotelsData = loadHotelsData()
    serverData = [usersData, hotelsData]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        cls()
        print("Server is starting...")
        s.bind(ADDR)
        print(f"Server is hosting on {IP}:{PORT}")
        s.listen()
        print("Waiting for connected...")
        conn, addr = s.accept()
        guest = ' '
        with conn:
            print(f"Connected by {addr}")
            while True:
                prosCode = recvMsg(conn)
                if prosCode == '0':
                    print("Client disconnected!")
                    break
                elif prosCode == '1': guest = checkLogin(conn, serverData)
                elif prosCode == '2': addAccount(conn, serverData)
                elif prosCode == '3': findHotel(conn, serverData)
                elif prosCode == '4': bookingHotel(conn, serverData,guest)
        s.close()

main()