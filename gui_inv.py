from PyQt5.QtWidgets import QVBoxLayout, \
    QPushButton, QComboBox, QGridLayout, QLabel, QTableView,QHBoxLayout, QHeaderView, QMenu, QAction, QLineEdit,  QTableWidgetItem,  QTableWidget
class Ui_Widget1(object):

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")

        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('File')

        self.impMenu = QMenu('Import', self)
        self.ExpMenu = QMenu('Eksport', self)
        self.search = QMenu('Wyświetl', self)
        self.Excel = QAction('Excel', self)
        self.Excelread = QAction('Excel', self)
        self.empty = QAction('Brakujące', self)
        self.pdf = QAction('PDF', self)
        self.all = QAction('Wszystkie', self)
        self.fileMenu.addMenu(self.search)
        self.search.addAction(self.empty)
        self.search.addAction(self.all)
        self.fileMenu.addMenu(self.impMenu)
        self.fileMenu.addMenu(self.ExpMenu)
        self.ExpMenu.addAction(self.pdf)
        self.ExpMenu.addAction(self.Excel)
        self.impMenu.addAction(self.Excelread)

        # właściwości widżetu ###
        self.setWindowTitle("Inwentarz")
        self.resize(740, 300)

class Ui_Widget1_cen(object):

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")

        # tabelaryczny widok danych
        self.widok = QTableView()

        self.editBtn = QPushButton("Edytuj", self)
        self.addBtn = QPushButton("Dodaj", self)
        self.delBtn = QPushButton("Usuń", self)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Lp."))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Nazwa"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("JM"))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Ilość"))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem("Cena"))
        self.tableWidget.setHorizontalHeaderItem(5, QTableWidgetItem("Wartość"))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().hide()

        self.layout = QVBoxLayout()
        self.Hlayout = QHBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.Hlayout.addWidget(self.addBtn)
        self.Hlayout.addWidget(self.editBtn)
        self.Hlayout.addWidget(self.delBtn)
        self.layout.addLayout(self.Hlayout)
        self.setLayout(self.layout)





        self.clsBtn = QPushButton("Koniec")


        uklad = QHBoxLayout()
        uklad.addWidget(self.clsBtn)

        # główny układ okna ###
        ukladV = QVBoxLayout(self)
        ukladV.addWidget(self.widok)
        ukladV.addLayout(uklad)



        self.resize(500, 300)


class SelUi(object):

    def setupUi(self, Widget):
        self.Lab1 = QLabel('Nazwa:')
        self.combo = QComboBox()
        self.thisBtn = QPushButton("Wybierz", self)
        self.addBtn = QPushButton("Dodaj", self)
        self.clsBtn = QPushButton("Zamknij", self)

        layout = QVBoxLayout()
        layout.addWidget(self.combo)
        layout.addWidget(self.thisBtn)
        layout.addWidget(self.clsBtn)

        uklad = QGridLayout(self)
        uklad.addWidget(self.Lab1, 0, 0)
        uklad.addWidget(self.combo, 1, 0, 1, 0)
        uklad.addWidget(self.thisBtn, 2, 0)
        uklad.addWidget(self.addBtn, 2, 1)
        uklad.addWidget(self.clsBtn, 2, 2)

        ukladV = QVBoxLayout(self)
        ukladV.addLayout(layout)


        self.setWindowTitle("Inwentarz")
        self.setFixedSize(330, 90)


class Addinv(object):

    def setupUi(self, Widget):
        self.Labc = QLabel('Kod:')
        self.code = QLineEdit()
        self.Labn = QLabel('Nazwa:')
        self.name = QLineEdit()
        self.Labjm = QLabel('JM:')
        self.JM = QLineEdit()
        self.Labam = QLabel('Ilość:')
        self.am = QLineEdit()
        self.Labprz = QLabel('Cena:')
        self.prize = QLineEdit()
        self.addBtn = QPushButton("Dodaj", self)

        layout = QVBoxLayout()

        uklad = QGridLayout(self)
        uklad.addWidget(self.Labc, 0, 0)
        uklad.addWidget(self.code, 0,1)
        uklad.addWidget(self.Labn, 1, 0)
        uklad.addWidget(self.name, 1,1)
        uklad.addWidget(self.Labjm, 2, 0)
        uklad.addWidget(self.JM, 2,1)
        uklad.addWidget(self.Labam, 3, 0)
        uklad.addWidget(self.am, 3,1)
        uklad.addWidget(self.Labprz, 4, 0)
        uklad.addWidget(self.prize, 4,1)
        uklad.addWidget(self.addBtn, 5,0,1,0)

        ukladV = QVBoxLayout(self)
        ukladV.addLayout(layout)
        self.code.setFocus()

        self.setWindowTitle("Inwentarz")
        self.setFixedSize(400, 175)

class AddEd(object):

    def setupUi(self, Widget):
        self.Labn = QLabel('Nazwa:')
        self.name = QLineEdit()
        self.Labjm = QLabel('JM:')
        self.JM = QLineEdit()
        self.Labam = QLabel('Ilość:')
        self.am = QLineEdit()
        self.Labprz = QLabel('Cena:')
        self.prize = QLineEdit()
        self.eddBtn = QPushButton("Edytuj", self)

        layout = QVBoxLayout()

        uklad = QGridLayout(self)
        uklad.addWidget(self.Labn, 1, 0)
        uklad.addWidget(self.name, 1,1)
        uklad.addWidget(self.Labjm, 2, 0)
        uklad.addWidget(self.JM, 2,1)
        uklad.addWidget(self.Labam, 3, 0)
        uklad.addWidget(self.am, 3,1)
        uklad.addWidget(self.Labprz, 4, 0)
        uklad.addWidget(self.prize, 4,1)
        uklad.addWidget(self.eddBtn, 5,0,1,0)

        ukladV = QVBoxLayout(self)
        ukladV.addLayout(layout)

        self.setWindowTitle("Inwentarz")
        self.setFixedSize(400, 150)

class IfExist(object):

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")

        # tabelaryczny widok danych
        self.widok = QTableView()
        self.Labname = QLabel('Nazwa: ')
        self.Labjm = QLabel('JM: ')
        self.addtoBtn = QPushButton("Dodaj do", self)
        self.addnewBtn = QPushButton("Dodaj nowe", self)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Ilość"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Cena"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Wartość"))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        self.tableWidget.verticalHeader().hide()

        self.layout = QVBoxLayout()
        self.Hlayout = QHBoxLayout()
        self.Llayout = QHBoxLayout()
        self.Llayout.addWidget(self.Labname)
        self.Llayout.addWidget(self.Labjm)
        self.layout.addLayout(self.Llayout)
        self.layout.addWidget(self.tableWidget)
        self.Hlayout.addWidget(self.addtoBtn)
        self.Hlayout.addWidget(self.addnewBtn)
        self.layout.addLayout(self.Hlayout)
        self.setLayout(self.layout)





        self.clsBtn = QPushButton("Koniec")


        uklad = QHBoxLayout()
        uklad.addWidget(self.clsBtn)

        # główny układ okna ###
        ukladV = QVBoxLayout(self)
        ukladV.addWidget(self.widok)
        ukladV.addLayout(uklad)


        self.setWindowTitle("Inwentarz")
        self.resize(324, 300)
class Impo(object):

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")

        # tabelaryczny widok danych
        self.widok = QTableView()

        self.addallBtn = QPushButton("Dodaj wszystkie", self)
        self.addselBtn = QPushButton("Dodaj wybrane", self)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Lp."))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Nazwa"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("JM"))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Ilość"))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem("Cena"))
        self.tableWidget.setHorizontalHeaderItem(5, QTableWidgetItem("Wartość"))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        self.tableWidget.verticalHeader().hide()

        self.layout = QVBoxLayout()
        self.Hlayout = QHBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.Hlayout.addWidget(self.addallBtn)
        self.Hlayout.addWidget(self.addselBtn)
        self.layout.addLayout(self.Hlayout)
        self.setLayout(self.layout)

        self.setWindowTitle("Inwentarz")
        self.resize(324, 300)
