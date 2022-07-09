from serverLib import *
import time
import array as arr
filename = "hotelsdata.json"


def view_Data(serverData):
    with open(filename,"r") as f:
        for i in serverData[1]['hotels']:
            if i == 'fivestar':
                print(i['rooms']['single']['listBooked'])
    return
##tui để define vậy

def get_Time():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)
    return

def deleteID(guest,serverData,s,idToDelete):
    for i in serverData[0]["username"]:
        if i == guest:
            del i["listBooked"][idToDelete]
    return

def showID(s,serverData,guest):
    number = arr.array('i',[])
    while True: ##cannot connect
        sendMsg(s,"Enter booking's ID that you want to cancel: ")
        recvMsg(s)
        for i in serverData[0]['users']:
            if i['username'] == guest:
                for j in i['listBooked']:
                    sendMsg(s,j['id'])
                    number.append(int(j['id']))
                    recvMsg(s)
                sendMsg(s,'outof')
        choice = recvMsg(s)
        print("ID to delete is: ",number[int(choice)-1]) ##SHOW Ra để kiểm chứng thôi :V
        idToDelete = number[int(choice)-1]  ##đây là cái biến ID cần delete
        deleteID(guest,serverData,s,idToDelete) ##làm từ đây đi... :V
        break
    return
