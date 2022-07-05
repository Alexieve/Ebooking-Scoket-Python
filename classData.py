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