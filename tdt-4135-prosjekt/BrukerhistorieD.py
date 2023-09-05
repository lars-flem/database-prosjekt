import sqlite3
import datetime


def togrute_mellom_stasjoner():
    con = sqlite3.connect("prosjektdatabase.db")
    cursor = con.cursor()
    
    start = input("Vennligst oppgi hvilken stasjon du vil reise fra: ")
    slutt = input("Hvilken stasjon vil du reise til?: ")
    dato = input("Hvilken dato vil du reise? (yyyy-mm-dd): ")
    tid = input("Hvilket tidspunkt vil du reise på? (hh:mm): ")
    
    try:
        dato_obj = datetime.datetime.strptime(dato, '%Y-%m-%d').date()
        dato_plus_one_day = (dato_obj + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date format: must be YYYY-MM-DD")
    try:
        time_obj = datetime.datetime.strptime(tid, '%H:%M').time()
    except ValueError:
        raise ValueError("Invalid time format: must be HH:MM")
    
    cursor.execute("""SELECT TogruteForekomst.RuteID, TogruteForekomst.Dato, StasjonIRute.Avgang 
                   FROM TogruteForekomst NATURAL JOIN StasjonIRute 
                   WHERE ((Dato = ? AND Avgang >= ?) or Dato = ?) AND StasjonNavn = ? AND RuteID IN 
                   (SELECT RuteID 
                   FROM TogruteForekomst NATURAL JOIN StasjonIRute 
                   WHERE StasjonNavn = ?) AND RuteID IN 
                   (SELECT a.RuteID 
                   FROM StasjonIRute AS a INNER JOIN StasjonIRute AS b ON (a.RuteID = b.RuteID) 
                   WHERE a.StasjonNavn = ? AND b.StasjonNavn = ? AND a.StasjonNr < b.StasjonNr)
                   ORDER BY Dato ASC, Avgang ASC""", (dato, tid, dato_plus_one_day, start, slutt, start, slutt))
    db1 = cursor.fetchall()
    print("Togrutene du kan ta fra", start, "til", slutt, "på datoene", dato, "og", dato_plus_one_day, "med avgang etter", dato+"/"+tid, "er: ")
    for i in range(0,len(db1)):
        print("Rute:", db1[i][0], "Klokka", db1[i][2], "på datoen", db1[i][1])
            