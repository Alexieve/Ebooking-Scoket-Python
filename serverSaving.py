from serverLib import *

def addingUserData(serverData, username, password, cardID):
    with open("usersdata.json") as file:
        data = json.load(file)
        listUsers = data["users"]
        user = users(username, password, cardID)
        userJson = {'username': user.username, 'password': user.password, 'cardID': user.cardID,
                    'listBooked': user.listBooked}
        listUsers.append(userJson)
    serverData[0] = data
    saveUsersData(serverData[0])
    print("Adding account complete!")

def addingUserBooked(id, guest, serverData):
    with open("usersdata.json") as file:
        data = json.load(file)
        listUsers = data["users"]
        for i in listUsers:
            if i['username'] == guest:
                userListBooked = i['listBooked']
                bookedDataJson = {'id': id}
                userListBooked.append(bookedDataJson)
    serverData[0] = data
    saveUsersData(serverData[0])
    print("Adding user's ID complete!")

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