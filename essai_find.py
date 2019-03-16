# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'essai_find.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setStyleSheet("border-color: rgb(179, 179, 179);\n"
                                 "border-top-color: rgb(252, 2, 128);")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 5, 1, 1)
        self.pushButton_update = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_update.setObjectName("pushButton_update")
        self.gridLayout.addWidget(self.pushButton_update, 2, 4, 1, 1)
        self.lineEdit_search = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.gridLayout.addWidget(self.lineEdit_search, 0, 0, 1, 1)
        self.comboBox_Aircraft = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_Aircraft.setObjectName("comboBox_Aircraft")
        self.gridLayout.addWidget(self.comboBox_Aircraft, 0, 4, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 2, 1, 1)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 6)
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 0, 1, 1, 1)
        self.dateEdit_2 = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.gridLayout.addWidget(self.dateEdit_2, 0, 2, 1, 1)
        self.rmv_btn = QtWidgets.QPushButton(self.centralwidget)
        self.rmv_btn.setObjectName("rmv_btn")
        self.gridLayout.addWidget(self.rmv_btn, 2, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
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
        self.label.setToolTip(_translate("MainWindow", "update me"))
        self.label.setText(_translate("MainWindow", "update with button"))
        self.pushButton_update.setToolTip(_translate("MainWindow", "mettre à jour la colonne total"))
        self.pushButton_update.setWhatsThis(_translate("MainWindow", "mettre à jour les heures"))
        self.pushButton_update.setText(_translate("MainWindow", "UPDATE"))
        self.pushButton.setText(_translate("MainWindow", "ADD"))
        self.dateEdit.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd"))
        self.dateEdit_2.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd"))
        self.rmv_btn.setText(_translate("MainWindow", "REMOVE"))
