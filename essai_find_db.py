#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtSql import *


class essaiFindDb():

    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("essai_find_database.db")

        self.db.open()

        query = QSqlQuery()
        # query.exec_('''CREATE TABLE Pilots(id INTEGER PRIMARY KEY,pilot_1 TEXT, datetime1 TEXT, datetime2 TEXT,pilot_mail TEXT)''')
        query.exec_('''CREATE TABLE Pilots_exp(id INTEGER PRIMARY KEY UNIQUE , pilot_1 TEXT,aircraft TEXT,
         date_time1 TEXT, date_time2 TEXT, total TEXT)''')

        query.exec_(
            '''CREATE TABLE Aircraft(id INTEGER PRIMARY KEY, immatriculation TEXT)''')

        query.exec_('''INSERT INTO Pilots_exp (id ,pilot_1, aircraft, date_time1 , date_time2, total )  VALUES 
        ( 1,'NOM','F-GTPH','2030/01/01 15:00','2030/01/01 16:00', '0')''')

        query.exec_('''INSERT INTO Aircraft(id, immatriculation) VALUES (1, 'F-GTPH')''')

        query.exec_()

        self.db.commit()
        self.db.close()


if __name__ == '__main__':
    essaiFindDb()

