from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDialog, QInputDialog, QMainWindow, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt
from gui import Ui_Widget
from gui_inv import Ui_Widget1, SelUi, Ui_Widget1_cen, Addinv, AddEd, IfExist, Impo
from gui_add import Ui_Widget2, Addclicked
from pdf import zy
from excel import create, read
import database


class MainWindow(QWidget, Ui_Widget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.clsBtn.clicked.connect(self.clos)
        self.invBtn.clicked.connect(self.invclicked)
        self.addBtn.clicked.connect(self.addclicked)

        try:
            Add_inv.kode
        except AttributeError:
            Add_inv.kode = 0
            QMessageBox.information(self, "Uwaga",
                                    "Program znajduje się w fazie beta testów,\npewne fragmenty nie są skończone lub nie gwarantują poprawnego działania\nwszelkie uwagi lub błędy proszę zgłaszać do dostawcy oprogramowania",
                                    QMessageBox.Ok)

        ThirdWindow.kodyk = Add_inv.kode

    def invclicked(self):
        MW.close()
        self.SW = SelectWindow()
        self.SW.show()

    def addclicked(self):
        MW.close()
        self.TW = ThirdWindow()
        self.TW.show()

    def clos(self):
        odp = QMessageBox.question(
            self, 'Komunikat',
            "Czy na pewno koniec?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if odp == QMessageBox.Yes:
            self.close()

class SelectWindow(QWidget, SelUi):                                                #wybor bazy do rem
    def __init__(self):
        super(SelectWindow, self).__init__()
        self.setupUi(self)
        self.clsBtn.clicked.connect(self.clos)
        self.addBtn.clicked.connect(self.add)
        self.thisBtn.clicked.connect(self.thisa)
        database.adda()
        tblist = database.gettb()
        tblist.remove('kody')
        tblist.remove('remanent')
        self.combo.addItems(tblist)
        SecondWindow.db = ''


    def thisa(self):
        SecondWindow.db = self.combo.currentText()
        self.close()
        self.SW = SecondWindow()
        self.SW.show()
    def add(self):
        name, ok = QInputDialog.getText(self, 'Nazwa', 'Podaj nazwe:')
        if ok:
            name = name.replace(" ", "")
            name = name.lower()
            z = name.isalnum()
            if z:
                x = name[0]
                try:
                    float(x)
                    QMessageBox.warning(self, "Błąd", "Pierwszy znak musi być literą", QMessageBox.Ok)
                    self.add()
                except ValueError:
                    tblist = database.gettb()
                    if tblist.count(str(name)) == 0:
                        database.chng(name)
                        SecondWindow.db = name
                        self.close()
                        self.SW = SecondWindow()
                        self.SW.show()
                    else:
                        QMessageBox.warning(self, "Błąd", "Taka nazwa już istnieje", QMessageBox.Ok)
                        self.add()
            else:
                QMessageBox.warning(self, "Błąd", "Nie może zawierać znaków specjalnych", QMessageBox.Ok)
                self.add()


    def clos(self):
        odp = QMessageBox.question(
            self, 'Komunikat',
            "Czy na pewno koniec?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if odp == QMessageBox.Yes:
            self.close()
            MW.show()
        else:
            pass


class SecondWindow(QMainWindow, Ui_Widget1):                                         # inv
    def __init__(self):
        super(SecondWindow, self).__init__()
        SecondWindow.tab = []
        SecondWindow.less = 0
        self.inside()
        self.setupUi(self)
        self.empty.triggered.connect(self.emptya)
        self.all.triggered.connect(self.alla)
        self.pdf.triggered.connect(self.ab)
        self.Excel.triggered.connect(self.ExcelCreate)
        self.Excelread.triggered.connect(self.ExcelRead)

    def inside(self):
        self.email_blast_widget = Sec_in(parent=self)
        self.setCentralWidget(self.email_blast_widget)

    def alla(self):
        SecondWindow.less = 0
        self.inside()

    def emptya(self):
        SecondWindow.less = 1
        self.inside()
    def ab(self):
        SecondWindow.less = 0
        self.inside()
        zy(SecondWindow.tab)
    def ExcelCreate(self):
        SecondWindow.less = 0
        self.inside()
        create(SecondWindow.tab)
    def ExcelRead(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","Excel(*.xls)", options=options)
        if files:
            SecondWindow.x = read(files)
            if SecondWindow.x == '0':
                QMessageBox.warning(self, "Błąd", "Sprawdź czy importujesz poprawny plik", QMessageBox.Ok)
            else:
                SecondWindow.res = QMessageBox.question(self, "Import", "Zsumować powtarzające się wartości?",
                                                QMessageBox.Yes | QMessageBox.No)

                self.Imp = Imp()
                self.Imp.exec_()
                SecondWindow.less = 0
                self.inside()


class Imp(QDialog, Impo):                                         #inv
    def __init__(self, parent=None):
        super(Imp, self).__init__(parent)
        self.setupUi(self)
        self.daba()

        self.addallBtn.clicked.connect(self.AddAll)
        self.addselBtn.clicked.connect(self.AddSel)

    def AddSel(self):
        q = set(index.row() for index in self.tableWidget.selectedIndexes())
        q = list(q)
        try:
            self.z = []
            for i in range(len(q)):
                self.z.append(['', '', '', '', '', ''])
                self.z[i][0] = self.tableWidget.item(q[i], 0).text()
                self.z[i][1] = self.tableWidget.item(q[i], 1).text()
                self.z[i][2] = self.tableWidget.item(q[i], 2).text()
                self.z[i][3] = self.tableWidget.item(q[i], 3).text()
                self.z[i][4] = self.tableWidget.item(q[i], 4).text()
                self.z[i][5] = self.tableWidget.item(q[i], 5).text()

        except AttributeError:
            QMessageBox.warning(self, "Błąd", "Element nie może być pusty", QMessageBox.Ok)
        if SecondWindow.res == QMessageBox.No:
            database.addimport(SecondWindow.db, self.z)
            self.close()
        else:
            database.addimportsame(SecondWindow.db, self.z)
            self.close()
    def AddAll(self):
        if SecondWindow.res == QMessageBox.No:
            database.addimport(SecondWindow.db, SecondWindow.x)
            self.close()
        else:
            database.addimportsame(SecondWindow.db, SecondWindow.x)
            self.close()

    def daba(self):
        db = SecondWindow.x
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(db):
            self.tableWidget.insertRow(row_number)
            q = []
            for i in range (0,6):
                q.append(row_data[i])
            row_data=q
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        model = self.tableWidget.model()
        data = []
        for row in range(model.rowCount()):
            data.append([])
            for column in range(model.columnCount()):
                index = model.index(row, column)
                data[row].append(str(model.data(index)))

class Sec_in(QWidget, Ui_Widget1_cen):                                         #inv
    def __init__(self, parent=None):
        super(Sec_in, self).__init__(parent)
        self.setupUi(self)
        self.daba()
        self.addBtn.clicked.connect(self.addy)
        self.editBtn.clicked.connect(self.eddy)
        self.delBtn.clicked.connect(self.delly)
    def daba(self):
        if SecondWindow.less == 0:
            db = database.gettable(SecondWindow.db)
        else:
            db = database.gettablea(SecondWindow.db)
        self.tableWidget.setRowCount(0);
        self.tableWidget.setRowCount(1)
        HowMuch = 1
        for row_number, row_data in enumerate(db):
            self.tableWidget.insertRow(row_number)
            q = []
            for i in range (0,5):
                q.append(row_data[i])
            q.insert(0, HowMuch)
            row_data=q
            HowMuch += 1
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        model = self.tableWidget.model()
        data = []
        for row in range(model.rowCount()):
            data.append([])
            for column in range(model.columnCount()):
                index = model.index(row, column)
                data[row].append(str(model.data(index)))
        SecondWindow.tab = data
    def addy(self):
        self.AI = Add_inv()
        self.AI.exec_()
        self.daba()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.eddy()
    def eddy(self):
        Sec_in.z = set(index.row() for index in self.tableWidget.selectedIndexes())
        if len(Sec_in.z) != 1:
            QMessageBox.warning(self, "Błąd", "Musisz wybrać jeden element do edycji", QMessageBox.Ok)
        else:
            try:
                self.z = []
                self.z.append(self.tableWidget.item(self.tableWidget.currentRow(), 1).text())
                self.z.append(self.tableWidget.item(self.tableWidget.currentRow(), 3).text())
                self.z.append(self.tableWidget.item(self.tableWidget.currentRow(), 4).text())
                Sec_in.z = self.z
                self.ED = Eddy()
                self.ED.exec_()
                self.daba()
            except AttributeError:
                QMessageBox.warning(self, "Błąd", "Element nie może być pusty", QMessageBox.Ok)


    def delly(self):
        Sec_in.q = set(index.row() for index in self.tableWidget.selectedIndexes())
        if len(Sec_in.q) != 1:
            QMessageBox.warning(self, "Błąd", "Musisz wybrać jeden element do edycji", QMessageBox.Ok)
        else:
            try:
                self.z = []
                self.z.append(self.tableWidget.item(self.tableWidget.currentRow(), 1).text())
                self.z.append(self.tableWidget.item(self.tableWidget.currentRow(), 3).text())
                self.z.append(self.tableWidget.item(self.tableWidget.currentRow(), 4).text())
                self.z.append(self.tableWidget.item(self.tableWidget.currentRow(), 2).text())
                Sec_in.q = Sec_in.q.pop() + 1
                self.res = QMessageBox.question(self, "Usuń", "Usunąc zazaczony element?", QMessageBox.Yes | QMessageBox.No)
                if self.res == QMessageBox.Yes:
                    database.dele(SecondWindow.db, self.z)
                    self.daba()
            except AttributeError:
                QMessageBox.warning(self, "Błąd", "Element nie może być pusty", QMessageBox.Ok)


class Eddy(QDialog, AddEd):                                         # dodaj  1
    def __init__(self, parent=None):
        super(Eddy, self).__init__(parent)
        self.setupUi(self)
        self.y = database.geted(str(SecondWindow.db), Sec_in.z)
        self.name.setText(self.y[1])
        self.JM.setText(self.y[2])
        self.am.setText(self.y[3])
        self.prize.setText(self.y[4])
        self.eddBtn.clicked.connect(self.edi)
    def edi(self):
        self.qy = list(self.y)
        self.q = 'Czy chcesz zmienić\n'
        if self.prize.text().__contains__(','):
            x = str(self.prize.text())
            x = x.replace(',', '.')
            self.prize.setText(x)
        if self.am.text()[0] == '0':
            self.am.setText(self.am.text()[1:])
        if self.prize.text()[0] == '0' and self.prize.text()[1] != '.':
            self.prize.setText(self.prize.text()[1:])

        if self.y[1] != self.name.text():
            self.q = 'Nazwe z: ' +self.y[1] + ' na: ' + str(self.name.text()) + '\n'
            self.qy[1] = str(self.name.text())
        if self.y[2] != self.JM.text():
            self.q = self.q +  'Jednostkę miary z: ' + self.y[2] + ' na: ' + str(self.JM.text()) + '\n'
            self.qy[2] = str(self.JM.text())
        if self.y[3] != self.am.text():
            self.q = self.q + 'Ilość z: ' + self.y[3] + ' na: ' + str(self.am.text()) + '\n'
            self.qy[3] = str(self.am.text())
        if self.y[4] != self.prize.text():
            self.prize.setText(str(round(float(self.prize.text()), 2)))
            self.q = self.q + 'Cenę z: ' + self.y[4] + ' na: ' + str(self.prize.text()) + '\n'
            self.qy[4] = str(self.prize.text())

        if self.q != 'Czy chcesz zmienić\n':
            try:
                x = int(self.am.text())
                y = float(self.prize.text())
                self.res = QMessageBox.question(self, "Zmiana", self.q,  QMessageBox.Yes | QMessageBox.No)
                if self.res == QMessageBox.Yes:
                    database.addedit(SecondWindow.db, self.qy)
                    QMessageBox.information(self, "Informacja", "Wartości zostały zmienione", QMessageBox.Ok)
                    self.close()
            except ValueError:
                QMessageBox.warning(self, "Błąd", "Ilość i ceną muszą być liczbami", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Informacja", "Nie zmieniono żadnej wartości", QMessageBox.Ok)


class Add_inv(QDialog, Addinv):
    def __init__(self):
        super(Add_inv, self).__init__()
        self.setupUi(self)
        self.addBtn.clicked.connect(self.addy)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.check()

    def check(self):
        x = self.code.text()
        try:
            int(x)
            q,y = database.checkis(x)
            if q != 0:
                self.name.setText(q)
                self.JM.setText(y)
                self.code.setReadOnly(True)
                self.name.setReadOnly(True)
                self.JM.setReadOnly(True)
                self.am.setFocus()
            else:
                QMessageBox.warning(self, "Błąd", "Nie ma takiego kodu w bazie", QMessageBox.Ok)
                Add_inv.kode = self.code.text()
                self.MW = MainWindow()
                self.AW = add1()
                self.AW.exec_()
                x, y = database.checkis(x)
                if x != 0:
                    self.name.setText(x)
                    self.JM.setText(y)
                    self.code.setReadOnly(True)
                    self.name.setReadOnly(True)
                    self.JM.setReadOnly(True)
                    self.am.setFocus()

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Błędny kod", QMessageBox.Ok)
            self.code.setText('')

    def addy(self):
        if self.prize.text() == '':
            self.prize.setText('0')
        if self.prize.text().__contains__(','):
            x = str(self.prize.text())
            x = x.replace(',', '.')
            self.prize.setText(x)
        try:
            int(self.am.text())
            z = float(self.prize.text())
            self.prize.setText(str(z))
            if self.name.text() == '' or self.JM.text() == '' or self.am.text() == '':
                QMessageBox.warning(self, "Błąd", "Nazwa, JM i ilość musi być podane", QMessageBox.Ok)
            else:
                x, xx = database.addtoinv(SecondWindow.db, self.name.text(), self.JM.text(), self.am.text(), self.prize.text())
                if x == 'a':
                    Add_inv.dates = xx
                    Add_inv.which = 0
                    Add_inv.edy = 0
                    self.AE = AddIfExist()
                    self.AE.exec_()
                    if Add_inv.which == 1:
                        database.addanother(SecondWindow.db, self.name.text(), self.JM.text(), self.am.text(),
                                            self.prize.text())
                        QMessageBox.information(self, "Uwaga",
                                                "Dodano: " + self.name.text() + "\nW ilości: " + self.am.text() + "\nW cenie: " + self.prize.text() + "\nO wartości: " + str(
                                                    round(int(self.am.text()) * float(self.prize.text()), 2)),
                                                QMessageBox.Ok)
                    if Add_inv.which == 2:
                        z = int(self.am.text()) + int(Add_inv.edy[2])
                        Add_inv.edy[2] = str(z)
                        x = float(Add_inv.edy[2]) * float(Add_inv.edy[3])
                        Add_inv.edy[4] = str(x)
                        database.addtoinvis(SecondWindow.db, Add_inv.edy)
                        QMessageBox.information(self, "Uwaga", "Zaktualizowano: " + self.name.text() + "\nW ilości: " + Add_inv.edy[2] + "\nO cenie: " + Add_inv.edy[3] + "\nO wartości: " + Add_inv.edy[4], QMessageBox.Ok)


                else:
                    QMessageBox.information(self, "Uwaga", "Dodano: " + self.name.text() + "\nW ilości: " + self.am.text() + "\nW cenie: " + self.prize.text() + "\nO wartości: " + str(round(int(self.am.text()) * float(self.prize.text()),2)), QMessageBox.Ok)
                self.code.setText('')
                self.name.setText('')
                self.JM.setText('')
                self.am.setText('')
                self.prize.setText('')
                self.code.setReadOnly(False)
                self.name.setReadOnly(False)
                self.JM.setReadOnly(False)
                self.code.setFocus()
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Ilość i cena muszą być liczbami", QMessageBox.Ok)



class AddIfExist(QDialog, IfExist):                                                     #dodaj 2
    def __init__(self):
        super(AddIfExist, self).__init__()
        self.setupUi(self)
        self.Labname.setText(self.Labname.text() + str(Add_inv.dates[0][1]))
        self.Labjm.setText(self.Labjm.text() + str(Add_inv.dates[0][2]))
        self.daba()
        self.addnewBtn.clicked.connect(self.AddNew)
        self.addtoBtn.clicked.connect(self.AddTo)

    def AddTo(self):
        q = set(index.row() for index in self.tableWidget.selectedIndexes())
        if len(q) != 1:
            QMessageBox.warning(self, "Błąd", "Musisz wybrać jeden element do edycji", QMessageBox.Ok)
        else:
            try:
                self.z = []
                self.z.append(str(Add_inv.dates[0][1]))
                self.z.append(str(Add_inv.dates[0][2]))
                self.z.append(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
                self.z.append(self.tableWidget.item(self.tableWidget.currentRow(), 1).text())
                self.z.append(self.tableWidget.item(self.tableWidget.currentRow(), 2).text())
                Add_inv.edy = self.z
                Add_inv.which = 2
                self.close()
            except AttributeError:
                QMessageBox.warning(self, "Błąd", "Element nie może być pusty", QMessageBox.Ok)

    def AddNew(self):
        Add_inv.which = 1
        self.close()


    def daba(self):
        print(Add_inv.dates)
        db = Add_inv.dates
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(db):
            self.tableWidget.insertRow(row_number)
            q = []
            for i in range (3,6):
                q.append(row_data[i])
            row_data=q
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        model = self.tableWidget.model()
        data = []
        for row in range(model.rowCount()):
            data.append([])
            for column in range(model.columnCount()):
                index = model.index(row, column)
                data[row].append(str(model.data(index)))

class ThirdWindow(QWidget, Ui_Widget2):                                         #dodaj  1
    def __init__(self, parent=None):
        super(ThirdWindow, self).__init__(parent)
        self.setupUi(self)
        self.clsBtn.clicked.connect(self.clos)
        self.addBtn.clicked.connect(self.add)


    def clos(self):
        self.close()

    def closeEvent(self, event):

        nadawca = self.sender()
        if nadawca != None and nadawca.text() == "Dodaj":
            event.accept()
        else:
            odp = QMessageBox.question(
                self, 'Komunikat',
                "Czy na pewno koniec?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if odp == QMessageBox.Yes:
                MW.show()
                event.accept()
            else:
                event.ignore()



    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.addBtn.click()
        if e.key() == Qt.Key_Escape:
            self.clsBtn.click()

    def add(self):
        try:
            cod = int(self.code.text())

            ThirdWindow.kodyk = cod

            self.ADDW = add1()
            self.ADDW.show()
            self.code.setText('')

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Błędne dane", QMessageBox.Ok)



class add1(QDialog, Addclicked):                                                     #dodaj 2
    def __init__(self):
        super(add1, self).__init__()
        self.setupUi(self)
        x = str(ThirdWindow.kodyk)
        self.codeLE.setText(str(x))
        self.check = database.check(str(self.codeLE.text()))

        if self.check != "":
            self.nameLE.setText(str(self.check[0]))
            self.measure.setText(str(self.check[1]))
            self.addtoBtn.setEnabled(False)
            self.combo.setEnabled(False)
        else:
            x = database.addto()
            self.combo.addItems(x)

        self.przyciski.accepted.connect(self.accept)
        self.przyciski.rejected.connect(self.reject)
        self.addtoBtn.clicked.connect(self.addto)

    def accept(self):
        if self.nameLE.text() == '':
            QMessageBox.warning(self, "Błąd", "Nie podałeś nazwy", QMessageBox.Ok)
        elif self.measure.text() =='':
            QMessageBox.warning(self, "Błąd", "Nie podałeś jednostki miary", QMessageBox.Ok)
        else:
            database.add(str(self.codeLE.text()), self.nameLE.text(), self.measure.text())
            QMessageBox.information(self,
                                    'Dodano', 'Dodano produkt: ' + self.nameLE.text() + "\nO kodzie: "+ self.codeLE.text() + "\n Jednostka miary: " + self.measure.text(), QMessageBox.Ok)
            self.close()

    def reject(self):
        QMessageBox.information(self,
                                'Anulowano', 'Nie dodano produktu', QMessageBox.Ok)
        self.close()


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_Return:
            self.accept()



    def closeEvent(self, event):
        nadawca = self.sender()
        if nadawca == None:
            QMessageBox.information(self,
                                    'Anulowano', 'Nie dodano produktu', QMessageBox.Ok)
            event.accept()
        else:
            event.accept()
    def addto(self):
        self.curr =self.combo.currentText()
        self.meas = database.add(str(self.codeLE.text()), self.curr, self.measure.text())
        QMessageBox.information(self,
                                'Dodano', 'Dodano produkt: ' + self.curr + "\nO kodzie: " + self.codeLE.text() + "\n Jednostka miary: " + self.meas,
                                QMessageBox.Ok)
        self.close()





if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    database.conn()
    MW = MainWindow()
    MW.show()
    sys.exit(app.exec_())
