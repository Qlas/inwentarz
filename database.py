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
    query = "SELECT nazwa,jedmiary,ilosc,cena,wartosc FROM " + x
    res = base.execute_sql(query)
    return res

def gettablea(x):
    query = "SELECT nazwa,jedmiary,ilosc,cena,wartosc FROM " + x + " WHERE wartosc = '0' OR cena = '0' OR wartosc = '0.0' OR cena = '0.0'"
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


def geted(db, x):
    query = "SELECT * FROM " + db + " WHERE nazwa = '" + str(x[0]) + "' AND ilosc ='" + str(x[1]) +"' AND cena ='" + str(x[2]) +  "'"
    res = base.execute_sql(query)
    x = res.fetchone()
    return x


def addtoinv(db, name, jm, am, prize):
    x = "SELECT * FROM " + db + " WHERE nazwa = '" + name + "' AND jedmiary = '" + jm + "'"
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
def addtoinvis(db, x ):
    q = "UPDATE "+ db  +" SET ilosc = '"+ str(x[2]) +"', wartosc = '" + x[4] + "' WHERE nazwa = '"+x[0]+"' AND jedmiary = '" + x[1] +"' AND cena = '" + x[3] + "'"
    base.execute_sql(q)

def addedit(db, x):
    z = int(x[3]) * float(x[4])
    q = "UPDATE " + db + " SET nazwa = '" + str(x[1]) + "', jedmiary = '" + str(x[2]) + "', ilosc = '" + str(x[3]) + "', cena = '" + str(x[4]) + "', wartosc = '" + str(z)  + "' WHERE id = '" + str(x[0]) + "'"
    base.execute_sql(q)


def addto():
    tab = []
    for z in kody.select().dicts():
        if tab.count(z['nazwa']) == 0:
            tab.append(z['nazwa'])
        else:
            pass
    tab.sort()
    return tab


def addanother(db, name, jm, am, prize):
    x = "SELECT * FROM " + db + " WHERE nazwa = '" + name + "'"
    res = base.execute_sql(x)
    q = res.fetchall()
    value = (int(am) * float(prize))
    value = round(value,2)
    query = "INSERT INTO "+ db +"(nazwa,jedmiary,ilosc,cena,wartosc) VALUES ('"+name+"','"+jm+"','"+am+"','"+prize+"','"+str(value)+"')"
    base.execute_sql(query)
    return "b", q

def dele(db, x):
    p = "SELECT * FROM " + db + " WHERE nazwa ='" + str(x[0]) + "' AND ilosc ='" + str(x[1]) +"' AND cena ='" + str(x[2]) +"' AND jedmiary = '" + str(x[3]) + "'"
    q = base.execute_sql(p)
    t = q.fetchall()
    t = t[0]
    query = "DELETE FROM " + db + " WHERE id = '" + str(t[0]) + "' AND nazwa ='" + str(x[0]) + "' AND ilosc ='" + str(x[1]) +"' AND cena ='" + str(x[2]) +"' AND jedmiary = '" + str(x[3]) + "'"
    base.execute_sql(query)

def addimport(db, tab):
    for i in range(len(tab)):
        z = tab[i]
        query = "INSERT INTO " + db + "(nazwa,jedmiary,ilosc,cena,wartosc) VALUES ('" + z[1] + "','" + z[2] + "','" + z[3] + "','" + z[4] + "','" + z[5] +"')"
        base.execute_sql(query)

def addimportsame(db, tab):
    for i in range(len(tab)):
        z = tab[i]
        t = []
        x = "SELECT * FROM " + db + " WHERE nazwa = '" + z[1] + "' AND jedmiary = '" + z[2] + "' AND cena ='" + z[4] + "'"
        q = base.execute_sql(x)
        t = q.fetchall()
        if t == []:
            query = "INSERT INTO " + db + "(nazwa,jedmiary,ilosc,cena,wartosc) VALUES ('" + z[1] + "','" + z[2] + "','" + z[3] + "','" + z[4] + "','" + z[5] +"')"
            base.execute_sql(query)
        else:
            t = t[0]
            p = int(z[3])
            o = int(t[3])
            z[3] = str(p+o)
            p = float(z[3])
            o = float(t[4])
            z[5] = str(round(p*o,2))
            q = "UPDATE " + db + " SET ilosc = '" + str(z[3]) + "', wartosc = '" + str(z[5]) + "' WHERE id = '" + str(t[0]) + "' AND nazwa = '" + z[1] + "' AND jedmiary = '" + z[2] + "' AND cena ='" + z[4] + "'"
            base.execute_sql(q)