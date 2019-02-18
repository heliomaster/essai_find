from PyQt5.QtWidgets import QMainWindow, QApplication, QStyledItemDelegate, QDateTimeEdit, QHeaderView,QTableView
from PyQt5.QtCore import pyqtSlot, Qt, QAbstractItemModel,QModelIndex, QDateTime,QDate, QRegExp, QSortFilterProxyModel, Qt,QTime
from datetime import datetime,timedelta,time

import sys
import sqlite3
import essai_find
from essai_find_db import *



class MainWindow(QMainWindow, essai_find.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.DB = essaiFindDb()
        self.db_model = QSqlRelationalTableModel()
        self.db_model.setTable('Pilots_exp')
        self.db_model.setEditStrategy(QSqlRelationalTableModel.OnFieldChange)
        self.db_model.setRelation(2, QSqlRelation('Aircraft', 'immatriculation', 'immatriculation'))
        self.db_model.select()
        # self.tableView.setModel(self.db_model)
        self.tableView.setColumnHidden(0, True)
        # self.tableView.resizeColumnsToContents()
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.custom_delegate = customDelegate()
        self.tableView.setItemDelegateForColumn(3, self.custom_delegate)
        self.tableView.setItemDelegateForColumn(4, self.custom_delegate)

        self.dateEdit.setCalendarPopup(True)
        self.dateEdit_2.setCalendarPopup(True)
        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit_2.setDate(QDate.currentDate())



        # self.label.setText('{} H {} M'.format(*self.hours_minutes()))
        # self.label.setText(str(self.last_col_filtered))
        # self.label.setText('{} H {} M'.format(*self.proxy_hours_minutes()))


        ############  PROXY MODEL ###############
        self.proxyModel = MySortFilterProxyModel(self)
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSourceModel(self.db_model)

        # self.proxyView = self.tableView
        # self.proxyView.setAlternatingRowColors(True)
        # self.proxyView.setModel(self.proxyModel)
        self.tableView.setModel(self.proxyModel)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(True)

        self.lineEdit_search.textChanged.connect(self.textFilterChanged)
        self.dateEdit.dateChanged.connect(self.dateFilterChanged)
        self.dateEdit_2.dateChanged.connect(self.dateFilterChanged)



        # self.filtered_row_count = self.proxyModel.rowCount()
        # self.textFilterChanged()
        # self.dateFilterChanged()


    def dateFilterChanged(self):
        self.proxyModel.setFilterMinimumDate(self.dateEdit.date())
        self.proxyModel.setFilterMaximumDate(self.dateEdit_2.date())
        print(self.dateEdit.date())
        print(self.dateEdit_2.date())

    def textFilterChanged(self):
        # syntax = QRegExp.PatternSyntax(
        #     self.filterSyntaxComboBox.itemData(
        #         self.filterSyntaxComboBox.currentIndex()))
        caseSensitivity = Qt.CaseInsensitive
        regExp = QRegExp(self.lineEdit_search.text(),caseSensitivity)
        self.proxyModel.setFilterRegExp(regExp)

#########   FILTER ROW  ##########
    def get_filtered_rows(self):
        print("rows in fitered view is {} ".format(self.proxyModel.rowCount()))
        print("rows in original model is {}".format(self.db_model.rowCount()))

    def last_col_filtered(self):
        """Gets all the data from the filtered model and returns last column i.e total hours """
        data = []
        for row in range(self.proxyModel.rowCount()):
            data.append([])
            for column in range(self.proxyModel.columnCount()):
                index = self.proxyModel.index(row, column)
                data[row].append(str(self.proxyModel.data(index)))
            data2 = [col[5] for col in data]
        # print(data)
        print(data2)
        return data2

    def convert_last_col_filtered(self):
             date =[datetime.strptime(x,"%H:%M:%S") for x in self.last_col_filtered()]
             liste1 = []
             for i in date:
                 dt = timedelta(hours=i.hour, minutes=i.minute, seconds=i.second)
                 liste1.append(dt)
             return (sum(liste1,timedelta()))

    def proxy_hours_minutes(self):
        """conversion of time delta get_tot_hours to hours"""
        td = self.convert_last_col_filtered()
        resultat = td.days*24 + td.seconds//3600 , (td.seconds//60)%60
        print('{} H {} M'.format(*resultat))
        return resultat

    def update_combobox_pilots(self):
        #Filling combox _avion
        query_aircraft = QSqlQuery("SELECT immatriculation FROM Aircraft")
        liste_ac = []
        while query_aircraft.next():
            aircraft = query_aircraft.value(0)
            liste_ac.append(aircraft)
        # self.comboBox_avion.addItems(liste_ac)
        # self.comboBox_sel_ac.addItems(liste_ac)
        return liste_ac

    def get_tot_hours(self):
        """select dates from database """
        query1 = QSqlQuery("SELECT date_time1,date_time2 FROM Pilots_exp")
        liste = []
        while query1.next():
            date1 = query1.value(0)
            date2 = query1.value(1)
            essai = datetime.strptime(date2, "%Y/%m/%d %H:%M") - datetime.strptime(date1, "%Y/%m/%d %H:%M")
            liste.append(essai)
        total = sum(liste,timedelta())
        return total

    def hours_minutes(self):
        """conversion of time delta get_tot_hours to hours"""
        td = self.get_tot_hours()
        # td = self.convert_last_col_filtered()
        resultat = td.days*24 + td.seconds//3600 , (td.seconds//60)%60
        print('{} H {} M'.format(*resultat))
        return resultat


    def get_hours_diff(self):
        query1 = QSqlQuery("SELECT date_time1,date_time2 FROM Pilots_exp")
        result = []
        while query1.next():
            date1 = query1.value(0)
            date2 = query1.value(1)
            diff = datetime.strptime(date2, "%Y/%m/%d %H:%M") - datetime.strptime(date1, "%Y/%m/%d %H:%M")
            result.append(str(diff))
        return result


    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.add_record()

    def add_record(self):
        row = self.db_model.rowCount()
        print(row)
        # self.db_model.insertRow(row)


    def update_record(self):
        """UPDATES EACH SQL ROW WITH TIME DELTA FROM PREVIOUS 2 COLUMNS"""
        # print(self.get_hours_diff())
        conn = sqlite3.connect("essai_find_database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Pilots_exp")
        rowids = [row[0] for row in cur.execute('SELECT rowid FROM Pilots_exp')]
        cur.executemany('UPDATE Pilots_exp SET total=? WHERE id=?',zip(self.get_hours_diff(),rowids))
        conn.commit()
        self.db_model.select()
        # print(self.get_tot_hours())


    @pyqtSlot()
    def on_pushButton_update_clicked(self):
        self.update_record()
        self.label.setText('{} H {} M'.format(*self.proxy_hours_minutes()))





class customDelegate(QStyledItemDelegate):
    """DELEGATE INSERT CUSTOM DATEEDIT IN CELL """

    def __init__(self, parent=None):
        super(customDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        date_edit = QDateTimeEdit(parent)
        date_edit.setDisplayFormat("yyyy/MM/dd HH:mm")
        date_edit.setDateTime(QDateTime.currentDateTime())

        date_edit.setCalendarPopup(True)
        return date_edit

    def setModelData(self, editor, model, index):
        value = editor.dateTime().toString("yyyy/MM/dd HH:mm")
        model.setData(index, value)

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        qdate = QDateTime().fromString(value, "yyyy/MM/dd HH:mm")
        editor.setDateTime(qdate)


class MySortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(MySortFilterProxyModel, self).__init__(parent)

        self.minDate = QDate()
        self.maxDate = QDate()


    def setFilterMinimumDate(self, date):
        self.minDate = date
        self.invalidateFilter()

    def filterMinimumDate(self):
        return self.minDate

    def setFilterMaximumDate(self, date):
        self.maxDate = date
        self.invalidateFilter()

    def filterMaximumDate(self):
        return self.maxDate

    def filterAcceptsRow(self, sourceRow, sourceParent):
        index0 = self.sourceModel().index(sourceRow, 1, sourceParent)
        index1 = self.sourceModel().index(sourceRow, 2, sourceParent)
        index2 = self.sourceModel().index(sourceRow, 3, sourceParent)
        # print(QDate().fromString(self.sourceModel().data(index2),"yyyy/MM/dd HH:mm"))
        # print(self.dateInRange(QDate().fromString((self.sourceModel().data(index2)))))
        # print( datetime.strptime(self.sourceModel().data(index2), "%Y/%m/%d %H:%M"))

        return ((self.filterRegExp().indexIn(self.sourceModel().data(index0)) >= 0
                 or self.filterRegExp().indexIn(self.sourceModel().data(index1)) >= 0)
                and self.dateInRange(datetime.strptime(self.sourceModel().data(index2),"%Y/%m/%d %H:%M")))

                # self.dateInRange(self.sourceModel().data(index2)))


    # def lessThan(self, left, right):
    #     leftData = self.sourceModel().data(left)
    #     rightData = self.sourceModel().data(right)
    #
    #     if not isinstance(leftData, QDate):
    #         emailPattern = QRegExp("([\\w\\.]*@[\\w\\.]*)")
    #
    #         if left.column() == 1 and emailPattern.indexIn(leftData) != -1:
    #             leftData = emailPattern.cap(1)
    #
    #         if right.column() == 1 and emailPattern.indexIn(rightData) != -1:
    #             rightData = emailPattern.cap(1)
    #
    #     return leftData < rightData

    def dateInRange(self, date):
        if isinstance(date, QDateTime):
            date = date.date()

        return ((not self.minDate.isValid() or date >= self.minDate)
                and (not self.maxDate.isValid() or date <= self.maxDate))



if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        form = MainWindow()
        # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        form.show()
        app.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error: ", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window....")
    except Exception:
        print(sys.exc_info()[1])
