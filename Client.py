from clientLib import *

IP = "127.0.0.1"
PORT = 1234
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def test(s): ##delete cái booking
    while True:
        print(recvMsg(s))
        sendMsg(s,'ok')
        i=1
        while True: ##dòng 14 đến dòng 19 là in ra các ID
            info = recvMsg(s)
            if info != 'outof':
                print(i,':',info)
                i+=1
                sendMsg(s, 'ok')
            else: break
        choice = input("I want: ")
        sendMsg(s,choice)
        waitForInput() ##tới đây thi đang tạm ngưng,có gì ông làm tiếp
        break




def showMenu(s):
    while True:
        cls()
        print("1. Book a room")
        print("2. Searching")
        print("3. Cancel Booking")
        print("0. Exit")
        choice = input('> ')
        if choice == '1':
            bookRoomMenu(s)
        elif choice == '2':
            searchingMenu(s)
        elif choice == '3':
            ##tui nghĩ là gọi hàm ở đây để te

            sendMsg(s,'5') ##
            test(s)
            ##cannot connect :")
            ## F
            ## F
            return
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