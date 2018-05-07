from peewee import *
base = SqliteDatabase('baza.db')


class DbModel(Model):

    class Meta:
        database = base


def gettb():
    z = base.get_tables()   #zbieramy nazwy tabel
    return z


def chng(name):
    base.execute_sql('alter table remanent rename to ' + name + ';')            # zmiana nazwy tab


class kody(DbModel):                                                                # tworzenie tab
    kod = CharField()
    nazwa = CharField()
    jedmiary = CharField()


class remanent(DbModel):                                                            # tworzenie tab
    nazwa = CharField()
    jedmiary = CharField()
    ilosc = CharField()
    cena = CharField()
    wartosc = CharField()


def adda():
    base.create_tables([remanent])
    base.commit()
    base.close()


def conn():
    base.connect()  # nawiązujemy połączenie z bazą
    base.create_tables([kody])  # tworzymy tabel
    base.commit()
    base.close()
    return True

def gettable(x):
    query = "SELECT * FROM " + x
    res = base.execute_sql(query)
    return res

def check(code):
    try:
        kody.get_or_create(kod = code)
        zec = kody.get(kody.kod == code).nazwa
        zyc = kody.get(kody.kod == code).jedmiary
        return zec, zyc
    except IntegrityError:
        return ""


def add(x,y,z):
    try:
        kody.get_or_create(kod=x)
        mdetails = kody.select().where(kody.kod == x).get()
        mdetails.nazwa = y
        mdetails.jedmiary = z
        mdetails.save()
    except IntegrityError:
        if z == '':
            mdetails = kody.select().where(kody.nazwa == y).get()
            z = mdetails.jedmiary

        zadanie = kody(kod = x, nazwa = y, jedmiary = z)
        zadanie.save()
        return z
def checkis(code):      #powtorzenie
    try:
        kody.get_or_create(kod=code)
        zec = kody.get(kody.kod == code).nazwa
        zyc = kody.get(kody.kod == code).jedmiary
        return zec,zyc

    except IntegrityError:
        return 0, 0


def geted(db, id):
    query = "SELECT * FROM " + db + " WHERE id = '" + id + "'"
    res = base.execute_sql(query)
    x = res.fetchone()
    return x


def addtoinv(db, name, jm, am, prize):
    x = "SELECT * FROM " + db + " WHERE nazwa = '" + name + "'"
    res = base.execute_sql(x)
    q = res.fetchall()
    if q == []:
        value = (int(am) * float(prize))
        value = round(value,2)
        query = "INSERT INTO "+ db +"(nazwa,jedmiary,ilosc,cena,wartosc) VALUES ('"+name+"','"+jm+"','"+am+"','"+prize+"','"+str(value)+"')"
        base.execute_sql(query)
        return "b", q
    else:
        return "a", q
def addtoinvis(db, x,y):
    k = x[3]
    z = int(k) + int(y)
    u = x[4]
    xx = z * float(u)
    xx = round(xx,2)
    xx = str(xx)
    z = str(z)
    q = "UPDATE "+db+" SET ilosc = '"+ z +"', wartosc = '" + xx + "' WHERE nazwa = '"+x[1]+"'"
    base.execute_sql(q)
    return z,xx

def addedit(db, x):
    z = int(x[3]) * float(x[4])
    q = "UPDATE " + db + " SET nazwa = '" + str(x[1]) + "', jedmiary = '" + str(x[2]) + "', ilosc = '" + str(x[3]) + "', cena = '" + str(x[4]) + "', wartosc = '" + str(z)  + "' WHERE id = '" + str(x[0]) + "'"
    base.execute_sql(q)
def addtoinvpr(db,x,y):
    k = x[3]
    z = int(k) + int(y)
    u = x[4]
    xx = z * float(u)
    xx = round(xx, 2)
    xx = str(xx)
    z = str(z)
    q = "UPDATE " + db + " SET ilosc = '" + z + "', wartosc = '" + xx + "', cena = '"+str(u)+"' WHERE nazwa = '" + x[1] + "'"
    base.execute_sql(q)
    return z, xx


def addto():
    tab = []
    for z in kody.select().dicts():
        if tab.count(z['nazwa']) == 0:
            tab.append(z['nazwa'])
        else:
            pass
    tab.sort()
    return tab