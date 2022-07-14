from serverLib import *

def idGenerator(name, type, serverData):
    id = 1
    hotel = serverData[1]['hotels'][0]
    for i in serverData[1]['hotels']:
        if i['name'] == name:
            hotel = i
            break
        id += 1
    id *= 100

    room = hotel['rooms']['single']
    if type == 'single':
        room = hotel['rooms']['single']
        id += 10
    elif type == 'couple':
        room = hotel['rooms']['couple']
        id += 20
    elif type == 'family':
        room = hotel['rooms']['family']
        id += 30

    idList = []
    for i in room['listBooked']:
        idList.append(int(i['id'][2]))
    idList.sort()
    idRoom = 1
    indexList = 0
    while indexList < len(idList):
        if idRoom == idList[indexList]:
            idRoom += 1
            indexList += 1
        else:
            break

    fid = str(id + idRoom)
    return fid

def getUserIndex(severData, guest):
    index = 0
    for i in severData[0]['users']:
        if i['username'] == guest:
            return index
        index += 1

def findHotelIndex(serverData, hotelName):
    check = False
    index = 0
    for i in serverData[1]['hotels']:
        if i['name'] == hotelName:
            check = True
            break
        index += 1
    if check:
        return index
    else:
        return False