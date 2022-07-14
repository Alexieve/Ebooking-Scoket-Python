class booked:
    def __init__(self, user, id, checkin, checkout, Note):
        self.user = user
        self.id = id
        self.checkin = checkin
        self.checkout = checkout
        self.Note = Note

class users:
    def __init__(self, username, password, cardID):
        self.username = username
        self.password = password
        self.cardID = cardID
        self.listBooked = []
        self.cart = []

class ordered:
    def __init__(self, id, hotelname, roomtype, price, checkin, checkout, timeBooked, Note):
        self.id = id
        self.hotelname = hotelname
        self.roomtype = roomtype
        self.price = price
        self.checkin = checkin
        self.checkout = checkout
        self.timeBooked = timeBooked
        self.Note = Note
