from serverLib import *

def addingUserData(serverData, username, password, cardID):
    with open("usersdata.json") as file:
        data = json.load(file)
        # listUsers = data["users"]
        user = users(username, password, cardID)
        userJson = {'username': user.username, 'password': user.password, 'cardID': user.cardID,
                    'listBooked': user.listBooked, 'cart': user.cart}
        data["users"].append(userJson)
    serverData[0] = data
    saveUsersData(serverData[0])
    print("Adding account complete!")

def addingUserCart(order, guest, serverData):
    with open("usersdata.json") as file:
        data = json.load(file)
        listUsers = data["users"]
        for i in listUsers:
            if i['username'] == guest:
                userListBooked = i['cart']
                cartDataJson = {'hotelname': order.hotelname, 'roomtype': order.roomtype,
                    'price': order.price, 'checkin': order.checkin, 'checkout': order.checkout, 'Note': order.Note}
                userListBooked.append(cartDataJson)
    serverData[0] = data
    saveUsersData(serverData[0])
    print("Adding user's order complete!")

def addingUserBooked(order, guest, serverData):
    with open("usersdata.json") as file:
        data = json.load(file)
        listUsers = data["users"]
        for i in listUsers:
            if i['username'] == guest:
                userListBooked = i['listBooked']
                bookedDataJson = {'id': order.id, 'hotelname': order.hotelname, 'roomtype': order.roomtype,
                    'price': order.price, 'checkin': order.checkin, 'checkout': order.checkout,
                    'timeBooked': order.timeBooked, 'Note': order.Note}
                userListBooked.append(bookedDataJson)
    serverData[0] = data
    saveUsersData(serverData[0])

    with open("hotelsdata.json") as file:
        data = json.load(file)
        hotelIndex = int(order.id[0]) - 1
        bookedDataJson = {'username': guest, 'id': order.id, 'checkin': order.checkin, 'checkout': order.checkout,
            'timeBooked': order.timeBooked, 'Note': order.Note}
        data['hotels'][hotelIndex]['rooms'][order.roomtype]['listBooked'].append(bookedDataJson)
        Empty = str(int(data['hotels'][hotelIndex]['rooms'][order.roomtype]['empty']) - 1)
        Booked = str(int(data['hotels'][hotelIndex]['rooms'][order.roomtype]['booked']) + 1)
        data['hotels'][hotelIndex]['rooms'][order.roomtype]['listBooked'].append(bookedDataJson)
        data['hotels'][hotelIndex]['rooms'][order.roomtype]['empty'] = Empty
        data['hotels'][hotelIndex]['rooms'][order.roomtype]['booked'] = Booked
    serverData[1] = data
    saveHotelsData(serverData[1])

    print("Adding user's booked complete!")

def saveUsersData(usersData):
    print("Saving users data...")
    with open("usersdata.json", 'w') as writeFile:
        json.dump(usersData, writeFile, indent=4)
    print("Saving complete!")

def saveHotelsData(hotelsData):
    print("Saving hotels data...")
    with open("hotelsdata.json", 'w') as writeFile:
        json.dump(hotelsData, writeFile, indent=4)
    print("Saving complete!")