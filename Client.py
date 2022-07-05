from clientLib import *

IP = "127.0.0.1"
PORT = 1234
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

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

def main():
    print("Connecting...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        cls()
        try:
            s.connect(ADDR)
            print(f"Connecting so server ({IP}:{PORT}) success!")
            waitForInput()
            while True:
                if not startingFunc(s):
                    break
                showMenu(s)
        except:
            print("Cannot connect to server!")

main()