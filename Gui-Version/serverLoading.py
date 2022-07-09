from serverLib import *

def loadUsersData():
    print("Loading users data...")
    with open("usersdata.json", "r") as readFile:
        usersData = json.load(readFile)
    print("Loading complete!")
    return usersData

def loadHotelsData():
    print("Loading hotels data...")
    with open("hotelsdata.json", "r") as readFile:
        hotelsData = json.load(readFile)
    print("Loading complete!")
    return hotelsData
