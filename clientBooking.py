from clientLib import *

def booking(s, hotelName):
    while True:
        print("--------------------------------")
        print("1.Single")
        print("---> Description:", recvMsg(s))
        sendMsg(s,'ok')
        print("---> Price:", recvMsg(s))
        sendMsg(s,'ok')
        print("---> Empty:",recvMsg(s))
        sendMsg(s,'ok')
        print("2.Couple")
        print("---> Description:", recvMsg(s))
        sendMsg(s, 'ok')
        print("---> Price:", recvMsg(s))
        sendMsg(s, 'ok')
        print("---> Empty:", recvMsg(s))
        sendMsg(s,'ok')
        print("3.Family")
        print("---> Description:", recvMsg(s))
        sendMsg(s, 'ok')
        print("---> Price:", recvMsg(s))
        sendMsg(s, 'ok')
        print("---> Empty:", recvMsg(s))
        sendMsg(s,'ok')
        numRoomType = input("The room type you want is: ")
        sendMsg(s, numRoomType)
        if numRoomType == '1':roomType = 'single'
        elif numRoomType == '2': roomType = 'couple'
        elif numRoomType == '3': roomType = 'family'

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
    i=1
    while True:
        name = recvMsg(s)
        if name == 'out': break
        print(i,":",name)
        sendMsg(s,'ok')
        i+=1
    numChoice = input("Hotel you want to book is: ")
    sendMsg(s,numChoice)
    hotelName = recvMsg(s)
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