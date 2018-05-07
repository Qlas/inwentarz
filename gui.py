from PyQt5.QtWidgets import QVBoxLayout, QPushButton

class Ui_Widget(object):

    def setupUi(self, Widget):
        self.invBtn = QPushButton("Inwentaryzacja", self)
        self.addBtn = QPushButton("Dodaj produkty", self)
        self.clsBtn = QPushButton("Zamknij", self)

        layout = QVBoxLayout()
        layout.addWidget(self.invBtn)
        layout.addWidget(self.addBtn)
        layout.addWidget(self.clsBtn)

        ukladV = QVBoxLayout(self)
        ukladV.addLayout(layout)



        self.setWindowTitle("Inwentarz")
        self.setFixedSize(400, 100)

