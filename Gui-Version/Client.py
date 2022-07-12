import datetime
import random

from clientLib import *
IP = "127.0.0.1"
PORT = 1234
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

class mainMenu(QtWidgets.QMainWindow, Ui_mainMenu):
    def goHome(self):
        # self.homePageShow(0)
        self.stackedWidget.setCurrentWidget(self.hotelpage)

    def checkPay(self):
        sendMsg(s, '12')
        check = recvMsg(s)
        sendMsg(s, "ok")
        if check == "None":
            self.showPopup("You have not book any room yet!")
            return
        data = json.loads(recvMsg(s))
        sendMsg(s, "ok")
        if data[3] != "True" and data[3] != "False":
            self.showPopup(data[3])
            self.cartindexnow = 0
            self.goCart()
            return
        self.user2.setText(data[0])
        self.room2.setText(str(data[1]))
        self.price72.setText(str(data[2]))
        self.stackedWidget.setCurrentWidget(self.paymentpage)

    def goCart(self):
        sendMsg(s, '7')
        self.getCartInformation(self.cartindexnow)
        self.stackedWidget.setCurrentWidget(self.cartpage)

    def goOrdered(self):
        sendMsg(s, '9')
        self.getOrderInformation(self.orderindexnow)
        self.stackedWidget.setCurrentWidget(self.cancelpage)

    def goSignout(self):
        self.close()

    def goSearch(self):
        sendMsg(s, '3')
        hotelname = self.inputhotel.text()
        if hotelname == "":
            hotelname = " "
        dateArrive = str(self.checkin.date().toPyDate())
        dateLeft = str(self.checkout.date().toPyDate())
        sendMsg(s, json.dumps([hotelname, dateArrive, dateLeft]))
        recvMsg(s)

        check = recvMsg(s)
        sendMsg(s, "ok")
        if check == "Hotel does not exits!":
            self.showPopup(check)
        else:
            self.getHotelInformation(check)
            check = recvMsg(s)
            sendMsg(s, "ok")
            if check != "True":
                self.showPopup(check)

    def goPay(self):
        sendMsg(s, '13')
        sendMsg(s, self.inputcardID.text())
        recvMsg(s)

        check = recvMsg(s)
        sendMsg(s, "ok")
        if check == "Some orders in the cart have been removed because there are no available rooms":
            self.showPopup(check)
            self.cartindexnow = 0
            self.goCart()
            return

        self.showPopup(check)
        if check == "Payment complete!":
            self.goHome()
            return
        elif check == "Wrong Card ID!":
            return
        self.cartindexnow = 0
        self.goCart()

    def bookingPageShow(self, roomType):
        sendMsg(s, '4')
        sendMsg(s, self.hotelname1.text())
        recvMsg(s)
        sendMsg(s, roomType)
        recvMsg(s)
        self.getBookingInformation(roomType)
        self.stackedWidget.setCurrentWidget(self.bookingpage)

    def orderPageShow(self, index):
        sendMsg(s, '9')
        self.orderindexnow += index
        self.getOrderInformation(self.orderindexnow)

    def cartPageShow(self, index):
        sendMsg(s, '7')
        self.cartindexnow += index
        self.getCartInformation(self.cartindexnow)

    def homePageShow(self, index):
        sendMsg(s, '5')
        self.hotelindexnow += index
        self.getHotelInformation(self.hotelindexnow)

    def addToCart(self):
        sendMsg(s, '6')
        hotelName = self.hotelname2.text()
        roomType = self.type2.text()
        checkin = str(self.dateEdit11.date().toPyDate())
        checkout = str(self.dateEdit_2.date().toPyDate())
        note = self.noteinput.text()
        if note == "":
            note = "None"
        sendMsg(s, json.dumps([hotelName, roomType, checkin, checkout, note]))
        recvMsg(s)
        check = recvMsg(s)
        sendMsg(s, "ok")
        self.showPopup(check)

    def editCart(self):
        sendMsg(s, '8')
        sendMsg(s, str(self.cartindexnow))
        recvMsg(s)
        check = recvMsg(s)
        sendMsg(s, "ok")
        if check == "False":
            self.showPopup("You have not book any room yet!")
            return
        checkin = str(self.dateEdit11_2.date().toPyDate())
        checkout = str(self.dateEdit_3.date().toPyDate())
        note = self.noteinput_2.text()
        sendMsg(s, json.dumps([checkin, checkout, note]))
        recvMsg(s)
        self.showPopup("Save complete!")

    def deleteOrderedRoom(self):
        sendMsg(s, '11', str(self.orderindexnow))
        recvMsg(s)
        check = recvMsg(s)
        sendMsg(s, "ok")
        if check == "None":
            self.showPopup("You have not book any room yet!")
            return

        check = recvMsg(s)
        sendMsg(s, "ok")
        if check == "False":
            self.showPopup("The cancellation time is over 24 hours")
            return
        self.showPopup("Remove complete!")
        self.orderPageShow(0)

    def deleteCartRoom(self):
        sendMsg(s, '10', str(self.cartindexnow))
        recvMsg(s)
        check = recvMsg(s)
        sendMsg(s, "ok")
        if check == "None":
            self.showPopup("You have not book any room yet!")
            return
        self.showPopup("Remove complete!")
        self.cartPageShow(0)

    def orderPageClickButton(self):
        self.cancelButton.clicked.connect(self.deleteOrderedRoom)
        self.prevButton2.clicked.connect(partial(self.orderPageShow, -1))
        self.nextButton2.clicked.connect(partial(self.orderPageShow, 1))

    def cartPageClickButton(self):
        self.cancelButton_2.clicked.connect(self.deleteCartRoom)
        self.payButton.clicked.connect(self.checkPay)
        self.payButton2.clicked.connect(self.goPay)
        self.editButton.clicked.connect(self.editCart)
        self.prevButton3.clicked.connect(partial(self.cartPageShow, -1))
        self.nextButton3.clicked.connect(partial(self.cartPageShow, 1))

    def bookingPageClickButton(self):
        self.acceptButton.clicked.connect(self.addToCart)
        self.backButton1.clicked.connect(self.goHome)

    def homePageClickButton(self):
        self.bookicon1.clicked.connect(partial(self.bookingPageShow, "single"))
        self.bookicon2.clicked.connect(partial(self.bookingPageShow, "couple"))
        self.bookicon3.clicked.connect(partial(self.bookingPageShow, "family"))
        self.prevButton.clicked.connect(partial(self.homePageShow, -1))
        self.nextButton.clicked.connect(partial(self.homePageShow, 1))

    def subClickButton(self):
        self.homeButton.clicked.connect(self.goHome)
        self.bookedButton.clicked.connect(self.goCart)
        self.usernameButton.clicked.connect(self.goOrdered)
        self.signoutButton.clicked.connect(self.goSignout)
        self.searchButton.clicked.connect(self.goSearch)

    def __init__(self, parent=None):
        super(mainMenu, self).__init__(parent=parent)
        self.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.mainArea.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        self.menuBar.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        self.systemlabel.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        self.searchButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))

        self.getInfor()
        self.subClickButton()
        self.homePageClickButton()
        self.bookingPageClickButton()
        self.cartPageClickButton()
        self.orderPageClickButton()
        self.stackedWidget.setCurrentWidget(self.hotelpage)

    def getOrderInformation(self, index):
        sendMsg(s, str(index))
        recvMsg(s)
        orderData = json.loads(recvMsg(s))
        sendMsg(s, "ok")
        if orderData == "None":
            self.prehotelname2.setText("None")
            self.type22.setText("None")
            self.des52.setText("None")
            self.price52.setText("None")
            self.showPopup("You have not book any room yet!")
            return
        self.prehotelname2.setText(orderData['hotelname'])
        self.type22.setText(orderData['roomtype'])
        self.des52.setText(orderData['id'])
        self.price52.setText(orderData['price'])
        checkin = datetime.strptime(orderData['checkin'], '%Y-%m-%d').date()
        checkout = datetime.strptime(orderData['checkout'], '%Y-%m-%d').date()
        self.checkin22.setDate(checkin)
        self.dateEdit_4.setDate(checkout)
        if orderData['Note'] != "None":
            self.note22.setText(orderData['Note'])
        image = json.loads(recvMsg(s))
        sendMsg(s, "ok")
        page = json.loads(recvMsg(s))
        sendMsg(s, "ok")
        self.imagetmp1.setPixmap(QtGui.QPixmap(image[0]))
        self.imageroom4.setPixmap(QtGui.QPixmap(image[1]))
        self.cartindexnow = int(page[0]) - 1
        self.pageCount1.setText(page[0] + '/' + page[1])

    def getCartInformation(self, index):
        sendMsg(s, str(index))
        recvMsg(s)
        orderData = json.loads(recvMsg(s))
        sendMsg(s, "ok")
        if orderData == "None":
            self.carthotelname2.setText("None")
            self.type32_2.setText("None")
            self.price62.setText("None")
            self.showPopup("You have not book any room yet!")
            return
        self.carthotelname2.setText(orderData['hotelname'])
        self.type32_2.setText(orderData['roomtype'])
        self.price62.setText(orderData['price'])
        checkin = datetime.strptime(orderData['checkin'], '%Y-%m-%d').date()
        checkout = datetime.strptime(orderData['checkout'], '%Y-%m-%d').date()
        self.dateEdit11_2.setDate(checkin)
        self.dateEdit_3.setDate(checkout)
        if orderData['Note'] != "None":
            self.noteinput_2.setText(orderData['Note'])
        image = json.loads(recvMsg(s))
        sendMsg(s, "ok")
        page = json.loads(recvMsg(s))
        sendMsg(s, "ok")
        self.imagetmp1.setPixmap(QtGui.QPixmap(image[0]))
        self.imageroom5.setPixmap(QtGui.QPixmap(image[1]))
        self.cartindexnow = int(page[0]) - 1
        self.pageCount2.setText(page[0] + '/' + page[1])

    def getBookingInformation(self, roomType):
        roomData = json.loads(recvMsg(s))
        sendMsg(s, "ok")

        self.hotelname2.setText(self.hotelname1.text())
        self.type2.setText(roomType)
        self.des42.setText(roomData['description'])
        self.price42.setText(roomData['price'])
        self.imageroom.setPixmap(QtGui.QPixmap(roomData['image']))

    def getHotelInformation(self, index):
        sendMsg(s, str(index))
        recvMsg(s)
        hotelData = json.loads(recvMsg(s))
        sendMsg(s, "ok")

        self.hotelname1.setText(hotelData['name'])
        self.imagetmp1.setPixmap(QtGui.QPixmap(hotelData['image']))

        single = hotelData['rooms']['single']
        self.des12.setText(single['description'])
        self.price12.setText(single['price'])
        self.empty11_2.setText(single['empty'])
        self.roomimage1.setPixmap(QtGui.QPixmap(hotelData['rooms']['single']['image']))

        couple = hotelData['rooms']['couple']
        self.des22.setText(couple['description'])
        self.price22.setText(couple['price'])
        self.empty22.setText(couple['empty'])
        self.roomimage2.setPixmap(QtGui.QPixmap(hotelData['rooms']['couple']['image']))

        family = hotelData['rooms']['family']
        self.des32.setText(family['description'])
        self.price32.setText(family['price'])
        self.empty32.setText(family['empty'])
        self.roomimage3.setPixmap(QtGui.QPixmap(hotelData['rooms']['family']['image']))

        page = json.loads(recvMsg(s))
        sendMsg(s, "ok")
        self.hotelindexnow = int(page[0]) - 1
        self.pageCount3.setText(page[0] + '/' + page[1])

    def getInfor(self):
        username = recvMsg(s)
        sendMsg(s, "ok")
        self.imagetmp1.setScaledContents(True)
        self.imageroom.setScaledContents(True)
        self.imageroom5.setScaledContents(True)
        self.imageroom4.setScaledContents(True)
        self.roomimage1.setScaledContents(True)
        self.roomimage2.setScaledContents(True)
        self.roomimage3.setScaledContents(True)
        self.cartindexnow = 0
        self.orderindexnow = 0
        self.hotelindexnow = 0
        self.usernameButton.setText(username)
        self.getHotelInformation(self.hotelindexnow)

    def showPopup(self, msg):
        QMessageBox.information(self, "Notification", msg)

class login(QtWidgets.QWidget, Ui_Login):
    def changeForm(self):
        if self.changeButton.isChecked():
            self.widget_2.hide()
            self.widget_3.show()
            self.changeButton.setText("<")
        else:
            self.widget_2.show()
            self.widget_3.hide()
            self.changeButton.setText(">")

    def showPopup(self, msg):
        QMessageBox.information(self, "Notification", msg)

    def __init__(self):
        super(login, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.label.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        self.label_3.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        self.loginButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3))
        self.regButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3))

        self.widget_3.hide()
        self.changeButton.clicked.connect(self.changeForm)
        self.loginButton.clicked.connect(self.loginFunction)
        self.regButton.clicked.connect(self.regFunction)

    def loginFunction(self):
        sendMsg(s, '1')
        username = self.userLoginInput.text()
        password = self.passLoginInput.text()
        if username == "" or password == "":
            username = " "
            password = " "
        sendMsg(s, json.dumps([username, password]))
        recvMsg(s)
        check = recvMsg(s)
        sendMsg(s, "ok")
        self.showPopup(check)
        if check == "Login success!":
            self.close()
            mainScreen = mainMenu(self)
            mainScreen.show()

    def regFunction(self):
        sendMsg(s, '2')
        username = self.userRegInput.text()
        password = self.passRegInput.text()
        confirm = self.confirmInput.text()
        cardID = self.cardIDInput.text()
        if username == "" or password == "" or confirm == "" or cardID == "":
            username = " "
            password = " "
            confirm = " "
            cardID = " "

        sendMsg(s, json.dumps([username, password, confirm, cardID]))
        recvMsg(s)
        check = recvMsg(s)
        self.showPopup(check)

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(ADDR)
            app = QApplication(sys.argv)
            loginScreen = login()
            loginScreen.show()
            app.exec_()
        except:
            app = QApplication(sys.argv)
            loginScreen = login().showPopup("Server is not active now!")