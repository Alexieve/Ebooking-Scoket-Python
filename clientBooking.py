from clientLib import *

def booking(s, hotelName):
    while True:
        print("--------------------------------")
        roomType = str(input("Room type: "))
        while True:
            if roomType != 'single' and roomType != 'couple' and roomType != 'family':
                roomType = str(input("No such room type.Type again here: "))
            else: break
        sendMsg(s, roomType)
        recvMsg(s)  ##Nhận tin nhắn OK bên Server
        ddmmyy(s)
        empty = recvMsg(s)
        if(empty == 'False'):
            print("This room type is full!")
            continue
        else:
            note = str(input("Note: "))
            sendMsg(s, note)
            break

def bookRoomMenu(s):
    sendMsg(s, '4')
    cls()
    print("Booking hotel:")
    while True:
        hotelName = str(input("Hotel name: "))
        sendMsg(s, hotelName)
        existHotel = recvMsg(s)
        if existHotel == 'False':
            print("No such hotel for you ! Type again")
            continue
        break

    while True:
        booking(s, hotelName)
        con = str(input("Continue to book ? (y/n): "))
        if con ==  'y':
            sendMsg(s,'continue')
            continue
        sendMsg(s, 'break')
        break

    price = recvMsg(s)
    cls()
    print("All the price is: ",price)
    while True:
        cardID = str(input("Enter your cardID to perform payment: "))
        sendMsg(s, cardID)
        checkID = recvMsg(s)
        if checkID == 'again':
            print("Wrong ID, type again!")
            continue
        break
    cls()