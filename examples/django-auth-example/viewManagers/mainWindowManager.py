from views.mainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from django.contrib.auth.models import User
from apps.accounts.models import Profile
from django.contrib.auth import authenticate


class mainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)
        self.addUserBtn.clicked.connect(self.addUser)
        self.authBtn.clicked.connect(self.authUser)
        try:
            user = User.objects.create_user('test', 'test@example.org', 'password')
            user.save()
            p = Profile.objects.get (user=user)
            p.bio = "BIO"
            p.save()
            print("USER 'test' CREATED")
        except Exception as e:
            print("Error : ", e)
    def addUser(self):
        username = self.username.text()
        password = self.password.text()
        email = username + "@example.org"
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            print("USER CREATED")
        except Exception as e:
            print(e)
    def authUser(self):
        username = self.username.text()
        password = self.password.text()
        user = authenticate(username=username, password=password)
        if user is not None:
            print("USER {} is authenticated".format(username))
        else:
            print("USER {} is NOT authenticated".format(username))

    def printUsers(self):
        allUsers = User.objects.all()
        print("Now we have {} users".format(len(allUsers)))
        print("Users : ")
        for user in allUsers:
            print(user.username)
