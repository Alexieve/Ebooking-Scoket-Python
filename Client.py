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
            print("Invalid password, try again!")
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