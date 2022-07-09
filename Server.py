from serverLib import *
IP = "127.0.0.1"
PORT = 1234
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

###### Processing code #####
# 0 Exit
# 1 Check login
# 2 Add account
# 3 Searching Hotels
# 4 Booking Hotels

def handleClient(conn, addr, serverData):
    print(f"[NEW CONNECTION] {addr} connected.")
    guest : str
    with conn:
        while True:
            prosCode = recvMsg(conn)
            if prosCode == '0':
                print(f"[DISCONNECT] Client {addr} disconnected!")
                break
            elif prosCode == '1':
                print(f"[REQUEST] Client {addr} ask to sign in:")
                guest = checkLogin(conn, serverData)
            elif prosCode == '2':
                print(f"[REQUEST] Client {addr} ask to sign up:")
                addAccount(conn, serverData)
            elif prosCode == '3':
                print(f"[REQUEST] Client {addr} ask to search hotel:")
                findHotel(conn, serverData)
            elif prosCode == '4':
                print(f"[REQUEST] Client {addr} ask to book a room:")
                bookingHotel(conn, serverData, guest)
            elif prosCode == '5':
                print(f"[REQUEST] Client {addr} ask to cancle booking:")
                showID(conn,serverData,guest)
    conn.close()

def main():
    cls()
    usersData = loadUsersData()
    hotelsData = loadHotelsData()
    serverData = [usersData, hotelsData]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        print("[STARTING] Server is starting...")
        server.bind(ADDR)
        print(f"[HOSTING] Server is hosting on {IP}:{PORT}")
        server.listen()
        print("[LISTENING] Waiting for connected...")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handleClient, args=(conn, addr, serverData))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

main()