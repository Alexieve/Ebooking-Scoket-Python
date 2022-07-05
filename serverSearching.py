from serverLib import *

def sendHotelsInfo(s, serverData, hotelName):
    dateArrive = datetime.datetime.strptime(recvMsg(s), "%d/%m/%y")
    dateLeft = datetime.datetime.strptime(recvMsg(s), "%d/%m/%y")
    fromClient(s)
    showRecvData(dateArrive, dateLeft)
    temp = 'single'
    ok = 1
    for i in serverData[1]['hotels']:
        if(i['name'] == hotelName):
            while True:
                empty = False
                haveBooked = False
                for j in i['rooms'][temp]['listBooked']:
                    haveBooked = True
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
    print(f"Sending hotels information for client {s.getpeername()} complete!")

def findHotel(s,serverData):
    print(f"Listening hotel's request from client {s.getpeername()}...")
    while True:
        hotelName = recvMsg(s)
        fromClient(s)
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