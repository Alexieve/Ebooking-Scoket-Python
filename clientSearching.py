from clientLib import *

def ddmmyy(s):
    dateArrive = str(input("Date arrive to hotel: (dd/mm/yy): "))
    dateLeft = str(input("Date left to hotel: (dd/mm/yy): "))
    sendMsg(s, dateArrive, dateLeft)

def hotelsInfo(s,hotelName):
    cls()
    print("Result after request:")
    print("Hotel name: ", hotelName)

    info1 = recvMsg(s)
    sendMsg(s, "CheckRecv")
    info2 = recvMsg(s)
    if (info1 != "NONE_INFO"):
        print("Single:")
        print("Description:", info1)
        print("Price:", info2)
    else:
        print("Single room now is not available")

    info1 = recvMsg(s)
    sendMsg(s, "CheckRecv")
    info2 = recvMsg(s)
    if (info1 != "NONE_INFO"):
        print("Couple:")
        print("Description:", info1)
        print("Price:", info2)
    else:
        print("Couple room now is not available")

    info1 = recvMsg(s)
    sendMsg(s, "CheckRecv")
    info2 = recvMsg(s)
    if (info1 != "NONE_INFO"):
        print("Family:")
        print("Description:", info1)
        print("Price:", info2)
    else:
        print("Family room now is not available")
    waitForInput()

def searchingMenu(s):
    sendMsg(s, '3')
    cls()
    print("Searching hotel:")
    while True:
        hotelName = str(input("Hotel name: "))
        sendMsg(s, hotelName)
        existHotel = recvMsg(s)
        if existHotel == "False":
            print("No such hotel for you ! Type again")
            continue
        break
    ddmmyy(s)
    hotelsInfo(s, hotelName)