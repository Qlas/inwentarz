from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDialog, QInputDialog, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from gui import Ui_Widget
from gui_inv import Ui_Widget1, SelUi, Ui_Widget1_cen, Addinv, AddEd
from gui_add import Ui_Widget2, Addclicked
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
                                    "Program znajduje się w wersji alfa,\npewne fragmenty nie są skończone lub nie gwarantują poprawnego działania\nwszelkie uwagi lub błędy proszę zgłaszać do dostawcy oprogramowania",
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

class SecondWindow(QMainWindow, Ui_Widget1):                                         #inv
    def __init__(self):
        super(SecondWindow, self).__init__()

        self.email_blast_widget = Sec_in(parent=self)
        self.setCentralWidget(self.email_blast_widget)
        self.setupUi(self)
        self.empty.triggered.connect(self.clos)



    def clos(self):
        odp = QMessageBox.question(
            self, 'Komunikat',
            "Czy na pewno koniec?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if odp == QMessageBox.Yes:
            self.close()
            MW.show()

class Sec_in(QWidget, Ui_Widget1_cen):                                         #inv
    def __init__(self, parent=None):
        super(Sec_in, self).__init__(parent)
        self.setupUi(self)
        self.daba()
        self.addBtn.clicked.connect(self.addy)
        self.editBtn.clicked.connect(self.eddy)
    def daba(self):
        db = database.gettable(SecondWindow.db)
        self.tableWidget.setRowCount(0);
        self.tableWidget.setRowCount(1)
        for row_number, row_data in enumerate(db):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
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
            Sec_in.z = Sec_in.z.pop() + 1
            self.ED = Eddy()
            self.ED.exec_()
            self.daba()



class Eddy(QDialog, AddEd):                                         #dodaj  1
    def __init__(self, parent=None):
        super(Eddy, self).__init__(parent)
        self.setupUi(self)
        self.y = database.geted(str(SecondWindow.db), str(Sec_in.z))
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
            float(self.prize.text())
            if self.name.text() == '' or self.JM.text() == '' or self.am.text() == '':
                QMessageBox.warning(self, "Błąd", "Nazwa, JM i ilość musi być podane", QMessageBox.Ok)
            else:
                if self.prize.text() == '0':
                    QMessageBox.information(self, "Uwaga", "nie podano ceny", QMessageBox.Ok)
                x, xx = database.addtoinv(SecondWindow.db, self.name.text(), self.JM.text(), self.am.text(), self.prize.text())
                if x == 'a':
                    res = QMessageBox.question(self, "Już istnieje", "Taka nazwa już istnieje w bazie, dodać ilość do niej?",  QMessageBox.Yes | QMessageBox.No)
                    if res == QMessageBox.Yes:
                        xxx = xx[0]
                        if xxx[4] != self.prize.text():
                            res2 = QMessageBox.question(self, "Cena się nie zgadza",
                                                       "Cena produktów jest inna, wpisać nową ("+ self.prize.text() +") zamiast starej ("+ xxx[4] +") ? \n (Yes - zamiana na nową, No - dodaje produkt ze starą cenę, Cancel - anuluje)",
                                                       QMessageBox.Yes | QMessageBox.No |QMessageBox.Cancel)
                            change = 2
                            if res2 == QMessageBox.Yes:
                                change = 1
                            elif res2 == QMessageBox.No:
                                change = 0
                            if change == 1 or change == 0:
                                if change == 1:
                                    zzz = (xxx[0],xxx[1],xxx[2],xxx[3],self.prize.text(),xxx[5])
                                    xxx = zzz
                                u, uu = database.addtoinvpr(SecondWindow.db, xxx, self.am.text())
                                QMessageBox.information(self, "Uwaga",
                                                        "Zaktualizowano: " + self.name.text() + "\nW ilości: " + str(
                                                            u) + "\nW cenie: " + xxx[4] + "\nO wartości: " + str(
                                                            uu), QMessageBox.Ok)

                        else:
                            u,uu = database.addtoinvis(SecondWindow.db, xxx, self.am.text())
                            QMessageBox.information(self, "Uwaga", "Zaktualizowano: " + self.name.text() + "\nW ilości: " + str(u) + "\nW cenie: " + self.prize.text() + "\nO wartości: " + str(uu), QMessageBox.Ok)
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
