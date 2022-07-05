import socket
import os
import datetime

IP = "127.0.0.1"
PORT = 1234
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024


##### PROCESS FUNCTIONS #####
def cls():
    os.system('cls')


def waitForInput():
    input("Press ENTER to continue...")


def sendMsg(s, *listMsg):
    for i in listMsg:
        s.sendall(bytes(i, FORMAT))


def recvMsg(s):
    return s.recv(SIZE).decode(FORMAT)


##### MAIN FUNCTIONS #####
def loginFunc(s):
    cls()
    sendMsg(s, '1')
    print(">>>LOGIN<<<")
    username = str(input("Username: "))
    password = str(input("Password: "))
    sendMsg(s, username, password)
    check = recvMsg(s)
    if check == "False":
        print("Wrong username or password!")
    else:
        print("Login success!")
    waitForInput()
    return check


def registerFunc(s):
    def checkValidUsername(username):
        if len(username) < 5:
            return False
        for i in username:
            if ('A' <= i and i <= 'Z') or ('a' <= i and i <= 'z') or ('0' <= i and i <= '9'):
                continue
            else:
                return False
        return True

    def checkValidPassword(password):
        if len(password) < 3:
            return False
        return True

    def checkValidCardID(cardID):
        if len(cardID) != 10:
            return False
        for i in cardID:
            if i < '0' or '9' < i:
                return False
        return True

    sendMsg(s, '2')
    while True:
        cls()
        print(">>>REGISTER<<<")
        username = str(input("Username: "))
        if not checkValidUsername(username):
            print("Invalid username, try again!")
            waitForInput()
            continue

        sendMsg(s, username)
        exits = recvMsg(s)
        if exits == "True":
            print("The username is already taken, please choose another username!")
            waitForInput()
            continue

        password = str(input("Password: "))
        if not checkValidPassword(password):
            print("Invalid password, try again!")
            waitForInput()
            continue

        cardID = str(input("Card ID: "))
        if not checkValidCardID(cardID):
            print("Invalid card ID, try again!")
            waitForInput()
            continue

        print("Registation complete!")
        sendMsg(s, password, cardID)
        waitForInput()
        return


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
    hotelsInfo(s,hotelName)

def booking(s,hotelName):
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
            sendMsg(s,note)
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
        booking(s,hotelName)
        con = str(input("Continue to book ? (y/n): "))
        if con ==  'y':
            sendMsg(s,'continue')
            continue
        sendMsg(s,'break')
        break
    price = recvMsg(s)
    cls()
    print("All the price is: ",price)
    while True:
        cardID = str(input("Enter your cardID to perform payment: "))
        sendMsg(s, cardID)
        checkID =  recvMsg(s)
        if checkID == 'again':
            print("Wrong ID, type again!")
            continue
        break
    cls()




def showMenu(s):
    while True:
        cls()
        print("1. Book a room")
        print("2. Searching")
        print("0. Exit")
        choice = input('> ')
        if choice == '1':
            bookRoomMenu(s)
        elif choice == '2':
            searchingMenu(s)
        elif choice == '0':
            return
        else:
            print("Invalid input, please try again!")
            waitForInput()
            continue


def startingFunc(s):
    while True:
        cls()
        print("1. Login")
        print("2. Resgister")
        print("0. Exit")
        choice = input('> ')
        if choice == '1':
            loginSuccess = loginFunc(s)
            if loginSuccess == "True":
                return True
        elif choice == '2':
            registerFunc(s)
        elif choice == '0':
            print("Goodbye!")
            sendMsg(s, '0')
            return False
        else:
            print("Invalid input, please try again!")
            waitForInput()
            continue


##### MAIN #####
def main():
    print("Connecting...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(ADDR)
        cls()
        print(f"Connecting so server ({IP}:{PORT}) success!")
        waitForInput()
        while True:
            if not startingFunc(s):
                break
            showMenu(s)
        s.close()


main()