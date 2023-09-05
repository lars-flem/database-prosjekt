from datetime import date
import sqlite3

def vis_fremtidige_kjøp():    
    #Sjekker om kundeNr er i databasen
    
    con = sqlite3.connect("prosjektdatabase.db")
    cursor = con.cursor()
    cursor.execute("SELECT Epost FROM Kunde")
    output=cursor.fetchall()
    cursor.close()
    
    #Gjør om fra liste med funt til til liste med int
    alle_epost=[x[0] for x in output]
    gyldig_epost=False
    while gyldig_epost==False:
        epost=input("Vennligst oppgi epost: ")
        if epost in alle_epost:
            gyldig_epost=True
        else:
            print("Ikke en gyldig epost, prøv på nytt")    

    #Henter ut alle kundeordre
    con3 = sqlite3.connect("prosjektdatabase.db")
    cursor3 = con3.cursor()
    cursor3.execute("""SELECT KundeNr
                    FROM Kunde
                    WHERE Epost = ?
                    """,
                    (epost,))
    out=cursor3.fetchall()
    kundeNr=out[0][0]
    cursor3.close()
    
    con2 = sqlite3.connect("prosjektdatabase.db")
    #today=str(date.today())
    today='2023-04-01'
    cursor2 = con2.cursor()
    cursor2.execute("""SELECT KundeOrdre.OrdreNr, KundeOrdre.KundeNr, KundeOrdre.RuteID, KundeOrdre.DatoKjøpt, KundeOrdre.TidKjøpt, KundeOrdre.StartStasjon,
                        KundeOrdre.SluttStasjon, KundeOrdre.Dato, BillettKjop.SetePlassNr, BillettKjop.SengPlassNr, Vognoppsett.VognNr
                        FROM KundeOrdre
                        INNER JOIN BillettKjop ON KundeOrdre.OrdreNr = BillettKjop.OrdreNr
                        LEFT JOIN Vognoppsett ON (Vognoppsett.SittevognRegNr = BillettKjop.SeteRegNr 
                                                OR (Vognoppsett.SittevognRegNr IS NULL AND BillettKjop.SeteRegNr IS NULL))
                                            AND (Vognoppsett.SovevognRegNr = BillettKjop.SengRegNr 
                                                OR (Vognoppsett.SovevognRegNr IS NULL AND BillettKjop.SengRegNr IS NULL))
                        WHERE KundeOrdre.KundeNr = ? 
                        AND KundeOrdre.Dato > ?;"""
,
                    (kundeNr,today,))
    alle_Ordre=cursor2.fetchall()
    cursor2.close()
    
    #Endrer fra tupler til liste
    
    alle_Ordre= [list(tup) for tup in alle_Ordre]
    
          

    if len(alle_Ordre)==0:
        print("Ingen kommende reiser for denne kunden")
    else:
        print("Her er alle dine kommende reiser:\n")
        print("{:<8} {:<10} {:<8} {:<8} {:<10} {:<12} {:<12} {:<10} {:<10} {:<8} {:<12}".format("OrdreNr.","KundeNr","RuteID", "Tid Kjøpt", "", "Fra", "Til", "AvreiseDato", "Sete", "Seng", "VognNr"))
        print("-----------------------------------------------------------------------------------------------------------------")
        for rad in alle_Ordre:
            rad = ["" if element is None else str(element) for element in rad]
            print("{:<8} {:<10} {:<8} {:<8} {:<10} {:<12} {:<12} {:<10} {:<10} {:<8} {:<12}".format(*rad))

    