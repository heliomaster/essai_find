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
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_date_1 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_date_1.setObjectName("comboBox_date_1")
        self.gridLayout.addWidget(self.comboBox_date_1, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 2, 1, 1)
        self.comboBox_date_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_date_2.setObjectName("comboBox_date_2")
        self.gridLayout.addWidget(self.comboBox_date_2, 0, 2, 1, 1)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 5)
        self.comboBox_pilot = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_pilot.setObjectName("comboBox_pilot")
        self.gridLayout.addWidget(self.comboBox_pilot, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setStyleSheet("border-color: rgb(179, 179, 179);\n"
"border-top-color: rgb(252, 2, 128);")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 4, 1, 1)
        self.comboBox_Aircraft = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_Aircraft.setObjectName("comboBox_Aircraft")
        self.gridLayout.addWidget(self.comboBox_Aircraft, 0, 3, 1, 1)
        self.pushButton_update = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_update.setObjectName("pushButton_update")
        self.gridLayout.addWidget(self.pushButton_update, 2, 3, 1, 1)
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
        self.pushButton.setText(_translate("MainWindow", "ADD"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton_update.setToolTip(_translate("MainWindow", "mettre à jour la colonne total"))
        self.pushButton_update.setWhatsThis(_translate("MainWindow", "mettre à jour les heures"))
        self.pushButton_update.setText(_translate("MainWindow", "UPDATE"))

