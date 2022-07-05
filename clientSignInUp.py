from clientLib import *

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