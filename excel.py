import xlwt
import xlrd
from datetime import datetime

def create(tab):
    # kodowanie arkusza
    book = xlwt.Workbook(encoding="utf-8")
    # tworzymy dowolną ilość arkuszy (zakładek)
    sheet1 = book.add_sheet("Inwentaryzacja")
    q = ["Lp.", "Nazwa", "JM", "Ilość", "Cena", "Wartość"]
    # umieszczamy w nich dane
    for i in range(len(q)):
        sheet1.write(0, i, q[i])
    for i in range(len(tab)-1):
        for j in range(len(tab[i])):
            sheet1.write(i+1, j, tab[i][j])

    # zapisujemy do pliku
    now = datetime.now()
    z = now.strftime("%Y-%m-%d")

    book.save("Inwentaryzacja " + z + ".xls")

def read(files):
    book = xlrd.open_workbook(files[0])
    for sheet_name in book.sheet_names():
        arkusz = book.sheet_by_name(sheet_name)
        if arkusz.row_values(0) == ['Lp.', 'Nazwa', 'JM', 'Ilość', 'Cena', 'Wartość']:
            x = 0
            z = 0
            tab = []
            while x == 0:
                try:
                    str(arkusz.row_values(z + 1))
                    tab.append(['','','','','',''])
                    for i in range(0,6):
                        tab[z][i] = arkusz.row_values(z + 1)[i]

                    z += 1
                except:
                    x = 1
            return tab
        else:
            return "0"
