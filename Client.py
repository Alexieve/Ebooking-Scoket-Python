import socket
import os

IP = "127.0.0.1"
PORT = 1234
ADDR = (IP, PORT)
FORMAT = 'utf-8'
SIZE = 1024

##### PROCESS FUNCTIONS #####
def cls():
    os.system('cls')
def waitForInput():
    input("Press ENTER to continue...")
def sendMsg(s, *listMsg):
    for i in listMsg:
        s.sendall(i.encode(FORMAT))
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
def registerFunc(s): # BUG
    sendMsg(s, '2')
    while True:
        cls()
        print(">>>REGISTER<<<")
        username = str(input("Username: "))
        if len(username) < 5:
            print("Invalid username, try again!")
            waitForInput()
            continue
        check = False
        for i in username:
            if (i >= 'A' and i <= 'Z') or (i >= 'a' and i <= 'z') or (i>= '0' and i <= '9'):
                continue
            else:
                print("Invalid username, try again!")
                waitForInput()
                check = True
                break
        if check:
            continue
        sendMsg(s, username)
        exits = recvMsg(s)
        if exits == "True":
            print("The username is already taken, please choose another username!")
            waitForInput()
            continue

        password = str(input("Password: "))
        if len(password) < 3:
            print("Password too short, try again!")
            waitForInput()
            continue

        cardID = str(input("Card ID: "))
        if len(cardID) != 10:
            print("Invalid card ID, try again!")
            waitForInput()
            continue
        check = False
        for i in cardID:
            if i < '0' or i > '9':
                print("Invalid card ID, try again!")
                waitForInput()
                check = True
                break
        if check:
            continue

        print("Registation complete!")
        sendMsg(s, password)
        sendMsg(s, cardID)
        waitForInput()
        break

def ddmmyy(s):
    dateArrive = str(input("Date arrive to hotel: (dd/mm/yyyy "))
    sendMsg(s,dateArrive)
    dateLeft = str(input("Date left to hotel: (dd/mm/yyyy "))
    sendMsg(s,dateLeft)


def searchingMenu(s):
    sendMsg(s, '3')
    cls()
    print("Searching hotel:")
    while True:
        hotelName = str(input("Hotel name: "))
        sendMsg(s, hotelName)
        existHotel = recvMsg(s)
        if existHotel == '0':
            print("No such hotel for you ! Type again")
            continue
    ddmmyy(s)
    cls()
    print("Result after request:")
    info = recvMsg(s)
    print("Hotel name: ",info)
    info = recvMsg(s)
    if(info != 'NONE_INFO'):
        print("Single: ")
        print("Description: ",info)
        info = recvMsg(s)
        print("Price: ",info)
    else: print("Singleroom now is not available")
    info = recvMsg(s)
    if (info != 'NONE_INFO'):
        print("Double: ")
        print("Description: ", info)
        info = recvMsg(s)
        print("Price: ", info)
    else:
        print("Singleroom now is not available")
    info = recvMsg(s)
    if (info != 'NONE_INFO'):
        print("Single: ")
        print("Description: ", info)
        info = recvMsg(s)
        print("Price: ", info)
    else:
        print("Singleroom now is not available")
    print("Press ENTER to continue...")
    waitForInput()

def bookRoomMenu(s):
    while True:
        sendMsg(s, '4')
        cls()
        print("Booking hotel:")
        hotelName = str(input("Hotel name: "))
        sendMsg(s, hotelName)
        existHotel = recvMsg(s)
        if existHotel == '0':
            print("No such hotel for you ! Type again")
            continue
    roomType = str(input("Room type: "))
    sendMsg(s,roomType)
    ddmmyy(s)


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
            s.send(b'0')
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