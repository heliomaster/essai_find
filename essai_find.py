# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'essai_find.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(40, 130, 591, 281))
        self.tableView.setObjectName("tableView")
        self.comboBox_pilot = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_pilot.setGeometry(QtCore.QRect(50, 60, 104, 26))
        self.comboBox_pilot.setObjectName("comboBox_pilot")
        self.comboBox_date_1 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_date_1.setGeometry(QtCore.QRect(180, 60, 104, 26))
        self.comboBox_date_1.setObjectName("comboBox_date_1")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 470, 60, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 470, 91, 16))
        self.label_2.setObjectName("label_2")
        self.comboBox_date_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_date_2.setGeometry(QtCore.QRect(300, 60, 104, 26))
        self.comboBox_date_2.setObjectName("comboBox_date_2")
        self.comboBox_Aircraft = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_Aircraft.setGeometry(QtCore.QRect(460, 60, 104, 26))
        self.comboBox_Aircraft.setObjectName("comboBox_Aircraft")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 460, 113, 32))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
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
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))

