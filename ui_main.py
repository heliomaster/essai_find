from PyQt5.QtWidgets import QMainWindow, QApplication, QStyledItemDelegate, QDateEdit
from PyQt5.QtCore import pyqtSlot,QDate, QDateTime,Qt


import sys

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
        self.db_model.setRelation(2,QSqlRelation('Aircraft','id','immatriculation'))
        self.db_model.select()
        self.tableView.setModel(self.db_model)
        self.custom_delegate = customDelegate()
        self.tableView.setItemDelegateForColumn(3,self.custom_delegate)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.add_record()

    def add_record(self):
        row = self.db_model.rowCount()
        self.db_model.insertRow(row)

class customDelegate(QStyledItemDelegate):
    """DELEGATE INSERT CUSTOM DATEEDIT IN CELL """

    def __init__(self, parent=None):
        super(customDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        date_edit = QDateEdit(parent)
        date_edit.setDisplayFormat("yyyy/MM/dd")
        date_edit.setDate(QDate.currentDate())

        date_edit.setCalendarPopup(True)
        return date_edit

    def setModelData(self, editor, model, index):
        value = editor.date().toString("yyyy/MM/dd")
        model.setData(index, value)

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        qdate = QDate().fromString(value, "yyyy/MM/dd")
        editor.setDate(qdate)



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