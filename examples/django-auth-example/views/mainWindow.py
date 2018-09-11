# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/zed/Desktop/proj/forms/mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(428, 242)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.username = QtWidgets.QLineEdit(self.page)
        self.username.setObjectName("username")
        self.verticalLayout_2.addWidget(self.username)
        self.password = QtWidgets.QLineEdit(self.page)
        self.password.setObjectName("password")
        self.verticalLayout_2.addWidget(self.password)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addUserBtn = QtWidgets.QPushButton(self.page)
        self.addUserBtn.setObjectName("addUserBtn")
        self.horizontalLayout.addWidget(self.addUserBtn)
        self.authBtn = QtWidgets.QPushButton(self.page)
        self.authBtn.setObjectName("authBtn")
        self.horizontalLayout.addWidget(self.authBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 428, 32))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addUserBtn.setText(_translate("MainWindow", "Add User"))
        self.authBtn.setText(_translate("MainWindow", "Auth"))

