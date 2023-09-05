import sqlite3
import random

def register_kunde():
    con = sqlite3.connect("prosjektdatabase.db")
    cursor = con.cursor()
    id = random.randint(0,100000000000)
    unik = 1
    while True:
        cursor.execute("SELECT KundeNr FROM Kunde")
        row = cursor.fetchall()
        for i in row:
            if i == id:
                unik = 0
                break
        if unik == 0:
            id = random.randint(0,10000000000)
        elif unik == 1:
            break
    print("Takk for at du vil registrere deg i våre systemer. Vennligst oppgi følgende data:")
    navn = input("Fullt Navn: ")
    tlf = input("Telefonnummer: ")
    epost = input("Epost: ")


    cursor.execute("""INSERT INTO Kunde VALUES (?, ?, ?, ?) """, ( id, navn, epost,tlf))
    print("Du er nå registrert som kunde!")
    con.commit()
    con.close()