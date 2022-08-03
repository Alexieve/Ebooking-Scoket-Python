from serverLib import *

def addingUserData(serverData, username, password, cardID):
    with open("Database\\usersdata.json") as file:
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
    with open("Database\\usersdata.json") as file:
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

def addingUserBooked(userData, hotelData, order, guest):
    data = hotelData
    hotelIndex = int(order.id[0]) - 1
    if not checkEmpty(data['hotels'][hotelIndex], order.roomtype, order.checkin, order.checkout):
        return [False, False]
    bookedDataJson = {'username': guest, 'id': order.id, 'checkin': order.checkin, 'checkout': order.checkout,
                      'timeBooked': order.timeBooked, 'Note': order.Note}
    Empty = str(int(data['hotels'][hotelIndex]['rooms'][order.roomtype]['empty']) - 1)
    Booked = str(int(data['hotels'][hotelIndex]['rooms'][order.roomtype]['booked']) + 1)
    data['hotels'][hotelIndex]['rooms'][order.roomtype]['listBooked'].append(bookedDataJson)
    data['hotels'][hotelIndex]['rooms'][order.roomtype]['empty'] = Empty
    data['hotels'][hotelIndex]['rooms'][order.roomtype]['booked'] = Booked
    hotelData = data

    data = userData
    indexUser = getUserIndex([userData, hotelData], guest)
    bookedDataJson = {'id': order.id, 'hotelname': order.hotelname, 'roomtype': order.roomtype,
        'price': order.price, 'checkin': order.checkin, 'checkout': order.checkout,
        'timeBooked': order.timeBooked, 'Note': order.Note}
    data['users'][indexUser]['listBooked'].append(bookedDataJson)
    userData = data

    print("Adding user's booked complete!")
    return [userData, hotelData]

def saveUsersData(usersData):
    print("Saving users data...")
    with open("Database\\usersdata.json", 'w') as writeFile:
        json.dump(usersData, writeFile, indent=4)
    print("Saving complete!")

def saveHotelsData(hotelsData):
    print("Saving hotels data...")
    with open("Database\\hotelsdata.json", 'w') as writeFile:
        json.dump(hotelsData, writeFile, indent=4)
    print("Saving complete!")