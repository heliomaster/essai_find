from PyQt5 import QtCore, QtGui, QtWidgets, QtSql

def createConnection():
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('essai_find_database.db')
    if not db.open():
        QtWidgets.QMessageBox.critical(None, QtWidgets.qApp.tr("Cannot open database"),
                             QtWidgets.qApp.tr("Unable to establish a database connection.\n"
                                     "This example needs SQLite support. Please read "
                                     "the Qt SQL driver documentation for information "
                                     "how to build it.\n\n"
                                     "Click Cancel to exit."),
                            QtWidgets.QMessageBox.Cancel)
        return False

    query = QtSql.QSqlQuery()
    return query.exec_('''
        CREATE TABLE IF NOT EXISTS Pilots_exp ( 
            id INTEGER PRIMARY KEY UNIQUE ,
            pilot_1 TEXT,aircraft TEXT, 
            date_time1 TEXT, date_time2 TEXT, 
            total TEXT)
        ''')

class ConvertToDateProxyModel(QtCore.QIdentityProxyModel):
    def __init__(self, parent=None):
        super(ConvertToDateProxyModel, self).__init__(parent)
        self._columns = []
        self._fmt = ""

    def set_format(self, fmt):
        self._fmt = fmt

    def set_columns(self, columns):
        self._columns = columns

    def data(self, index, role=QtCore.Qt.DisplayRole):
        v = super(ConvertToDateProxyModel, self).data(index, role)
        if not index.isValid():
            return
        if index.column() in self._columns and self._fmt:
            return QtCore.QDateTime.fromString(v, self._fmt)
        return v

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.column() in self._columns and self._fmt:
            sm = self.sourceModel()
            ix = self.mapToSource(index)
            return sm.setData(ix, value.toString(self._fmt), role)
        return super(ConvertToDateProxyModel, self).setData(index, value, role)

class FilterDateProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(FilterDateProxyModel, self).__init__(parent)
        self._from_date, self._to_date = QtCore.QDate(), QtCore.QDate()

    def setRange(self, from_date, to_date):
        self._from_date = from_date
        self._to_date = to_date
        self.invalidateFilter()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        if any([not date.isValid() for date in (self._from_date, self._to_date,)]):
            return True
        ix = self.sourceModel().index(sourceRow, self.filterKeyColumn(), sourceParent)
        dt = ix.data().date()
        return self._from_date <= dt <= self._to_date

class FilterTextProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(FilterTextProxyModel, self).__init__(parent)
        self._columns = []

    def set_columns(self, columns):
        self._columns = columns
        self.invalidateFilter()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        if not self._columns:
            return True
        values = []
        for c in range(self.sourceModel().columnCount()):
            if c in self._columns:
                ix = self.sourceModel().index(sourceRow, c, sourceParent)
                values.append(self.filterRegExp().indexIn(ix.data()) >= 0)
        return any(values)


class AddDialog(QtWidgets.QDialog):
    def __init__(self, formats, parent=None):
        super(AddDialog, self).__init__(parent)
        self._editors = dict()
        flay = QtWidgets.QFormLayout(self)
        for key, value in formats.items():
            editor = self.create_editor_by_type(value)
            flay.addRow(key, editor)
            self._editors[key] = editor

        buttonBox = QtWidgets.QDialogButtonBox()
        buttonBox.setOrientation(QtCore.Qt.Horizontal)
        buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        flay.addRow(buttonBox)

    def create_editor_by_type(self, t):
        editor = QtWidgets.QLineEdit()
        if t == QtCore.QDateTime:
            editor = QtWidgets.QDateTimeEdit(
                dateTime= QtCore.QDateTime.currentDateTime(),
                displayFormat="yyyy/MM/dd hh:mm",
                calendarPopup=True
            )
        return editor

    def get_value_from_editor(self, editor):
        if isinstance(editor, QtWidgets.QLineEdit):
            return editor.text()
        if isinstance(editor, QtWidgets.QDateTimeEdit):
            return editor.dateTime()

    def get_values(self):
        result = dict()
        for key, editor in self._editors.items():
            result[key] = self.get_value_from_editor(editor)
        return result

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self.db_model = QtSql.QSqlTableModel(self)
        self.db_model.setTable("Pilots_exp")
        self.db_model.select()

        proxy_convert_to_date = ConvertToDateProxyModel(self)
        proxy_convert_to_date.setSourceModel(self.db_model)
        proxy_convert_to_date.set_columns([3, 4])
        proxy_convert_to_date.set_format("yyyy/MM/dd hh:mm")

        sourceGroupBox = QtWidgets.QGroupBox("Original Model")
        sourceView = QtWidgets.QTableView(alternatingRowColors=True)
        sourceView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        sourceView.verticalHeader().hide()
        sourceView.setModel(proxy_convert_to_date)
        sourceLayout = QtWidgets.QHBoxLayout(sourceGroupBox)
        sourceLayout.addWidget(sourceView)

        self._proxy_date = FilterDateProxyModel(self)
        self._proxy_date.setFilterKeyColumn(3)
        self._proxy_date.setSourceModel(proxy_convert_to_date)

        self._proxy_filter = FilterTextProxyModel(self)
        self._proxy_filter.setSourceModel(self._proxy_date)
        self._proxy_filter.set_columns([1, 2])

        proxyGroupBox = QtWidgets.QGroupBox("Sorted/Filtered Model")
        proxyView = QtWidgets.QTableView()
        proxyView.verticalHeader().hide()
        proxyView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        proxyView.setSortingEnabled(True)
        proxyView.setModel(self._proxy_filter)
        proxyView.sortByColumn(1, QtCore.Qt.AscendingOrder)
        proxyLayout = QtWidgets.QVBoxLayout(proxyGroupBox)
        proxyLayout.addWidget(proxyView)

        filterPatternLabel = QtWidgets.QLabel("&Filter pattern:")
        self.filterPatternLineEdit = QtWidgets.QLineEdit(
            "Grace|Sports",
            textChanged=self.update_filter_text
        )
        filterPatternLabel.setBuddy(self.filterPatternLineEdit)
        self.filterSyntaxComboBox = QtWidgets.QComboBox(
            currentIndexChanged=self.update_filter_text
        )

        self.filterCaseSensitivityCheckBox = QtWidgets.QCheckBox(
            "Case sensitive filter",
            checked=True,
            stateChanged=self.update_filter_text
        )
        self.fromDateEdit = QtWidgets.QDateEdit(
            calendarPopup=True,
            date=QtCore.QDate(2006, 12, 22),
            dateChanged=self.update_filter_date
        )
        self.toDateEdit = QtWidgets.QDateEdit(
            calendarPopup=True,
            date=QtCore.QDate(2007, 1, 5),
            dateChanged=self.update_filter_date
        )

        self.filterSyntaxComboBox.addItem("Regular expression", QtCore.QRegExp.RegExp)
        self.filterSyntaxComboBox.addItem("Wildcard", QtCore.QRegExp.Wildcard)
        self.filterSyntaxComboBox.addItem("Fixed string", QtCore.QRegExp.FixedString)
        self.update_filter_text()
        self.update_filter_date()

        flay = QtWidgets.QFormLayout()
        flay.addRow("F&rom:", self.fromDateEdit)
        flay.addRow("&To:", self.toDateEdit)

        hlay = QtWidgets.QHBoxLayout()
        hlay.addWidget(filterPatternLabel)
        hlay.addWidget(self.filterPatternLineEdit)
        hlay.addWidget(self.filterSyntaxComboBox)
        proxyLayout.addWidget(self.filterCaseSensitivityCheckBox)
        proxyLayout.addLayout(hlay)
        proxyLayout.addLayout(flay)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(sourceGroupBox)
        lay.addWidget(proxyGroupBox)

        proxyView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        proxyView.customContextMenuRequested.connect(self.on_customContextMenuRequested)

    @QtCore.pyqtSlot(QtCore.QPoint)
    def on_customContextMenuRequested(self, p):
        view = self.sender()
        menu = QtWidgets.QMenu()
        add_row_action = menu.addAction("Add Row")
        action = menu.exec_(view.viewport().mapToGlobal(p))
        if action == add_row_action:
            self.add_record()

    @QtCore.pyqtSlot()
    def update_filter_text(self):
        syntax = self.filterSyntaxComboBox.currentData()
        caseSensitivity = QtCore.Qt.CaseSensitive \
            if self.filterCaseSensitivityCheckBox.isChecked() \
            else QtCore.Qt.CaseInsensitive
        regExp = QtCore.QRegExp(self.filterPatternLineEdit.text(), caseSensitivity, syntax)
        self._proxy_filter.setFilterRegExp(regExp)

    @QtCore.pyqtSlot()
    def update_filter_date(self):
        self._proxy_date.setRange(self.fromDateEdit.date(), self.toDateEdit.date())

    def add_record(self):
        d = {}
        rec = self.db_model.record()
        for i in range(rec.count()):
            d[rec.fieldName(i)] = type(rec.value(i))

        for i in (3, 4): d[rec.fieldName(i)] = QtCore.QDateTime

        del d[rec.fieldName(0)]

        dialog = AddDialog(d, self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            results = dialog.get_values()
            for i in (3, 4):
                k = rec.fieldName(i)
                results[k] = results[k].toString("yyyy/MM/dd hh:mm")
            for k, value in results.items():
                rec.setValue(k, value)
            self.db_model.insertRecord(-1, rec)
            self.db_model.select()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    if not createConnection():
        sys.exit(-1)
    w = Widget()
    w.resize(960, 480)
    w.show()
    sys.exit(app.exec_())