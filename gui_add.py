from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QDialogButtonBox, QGridLayout, QComboBox
from PyQt5.QtCore import Qt
class Ui_Widget2(object):

    def setupUi(self, Widget):


        self.et1 = QLabel("Kod:", self)
        self.code = QLineEdit()
        self.addBtn = QPushButton("Dodaj", self)
        self.clsBtn = QPushButton("Zamknij", self)


        layoutH = QHBoxLayout()
        layoutH.addWidget(self.et1)
        layoutH.addWidget(self.code)

        layout = QVBoxLayout()
        layout.addLayout(layoutH)
        layout.addWidget(self.addBtn)
        layout.addWidget(self.clsBtn)

        self.setLayout(layout)

        self.code.setFocus()


        self.setWindowTitle("Inwentarz")
        self.setFixedSize(400, 100)


class Addclicked(object):
    def setupUi(self, Widget):
        codeLbl = QLabel('Kod:')
        nameLbl = QLabel('Nazwa:')
        self.et2 = QLabel("Jednostka miary:")
        self.measure = QLineEdit()
        self.codeLE = QLineEdit()
        self.codeLE.setReadOnly(True)
        self.nameLE = QLineEdit()
        self.combo = QComboBox()
        self.addtoBtn = QPushButton("Dodaj do", self)
        self.przyciski = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)


        # układ główny ###
        uklad = QGridLayout(self)
        uklad.addWidget(codeLbl, 0, 0)
        uklad.addWidget(self.codeLE, 0, 1)
        uklad.addWidget(nameLbl, 1, 0)
        uklad.addWidget(self.nameLE, 1, 1)
        uklad.addWidget(self.et2, 2, 0)
        uklad.addWidget(self.measure, 2, 1)
        uklad.addWidget(self.addtoBtn, 3, 0)
        uklad.addWidget(self.combo, 3, 1)
        uklad.addWidget(self.przyciski, 4, 0, 4, 0)

        self.nameLE.setFocus()


        self.setModal(True)
        self.setWindowTitle('Inwentarz')