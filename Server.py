from serverLib import *
IP = "127.0.0.1"
PORT = 1234
ADDR = (IP, PORT)

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
                bookingHotel(conn, serverData)
            elif prosCode == '5':
                print(f"[REQUEST] Client {addr} ask to show hotel:")
                showNextHotel(conn, serverData)
            elif prosCode == '6':
                print(f"[REQUEST] Client {addr} ask to add to cart:")
                addToCart(conn, serverData, guest)
            elif prosCode == '7':
                print(f"[REQUEST] Client {addr} ask to show cart:")
                showCart(conn, serverData, guest)
            elif prosCode == '8':
                print(f"[REQUEST] Client {addr} ask to edit cart:")
                editCart(conn, serverData, guest)
            elif prosCode == '9':
                print(f"[REQUEST] Client {addr} ask to show ordered:")
                showOrdered(conn, serverData, guest)
            elif prosCode == '10':
                print(f"[REQUEST] Client {addr} ask to delete cart room:")
                deleteCartRoom(conn, serverData, guest)
            elif prosCode == '11':
                print(f"[REQUEST] Client {addr} ask to delete ordered room:")
                deleteOrderedRoom(conn, serverData, guest)
            elif prosCode == '12':
                print(f"[REQUEST] Client {addr} ask to check payment:")
                checkPayment(conn, serverData, guest)
            elif prosCode == '13':
                print(f"[REQUEST] Client {addr} ask to payment:")
                goPayment(conn, serverData, guest)
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