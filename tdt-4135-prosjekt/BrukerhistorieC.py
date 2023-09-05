import sqlite3

def alle_togruter_innom_stasjon():
    stasjonnavn = input("Skriv inn et stasjonnavn: ")
    ukedag=input("Dag (Eks: Mandag): ")
    ukedag= ukedag.capitalize()
    con = sqlite3.connect("prosjektdatabase.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM JernbaneStasjon WHERE StasjonNavn = ?", (stasjonnavn,))
    stasjon=cursor.fetchone()
    cursor.close()
    dager=[ "Mandag", "Tirsdag", "Onsdag", "Torsdag","Fredag", "Lørdag", "Søndag"]
    
    #Sjekker om stasjon og dag er gyldig
    if stasjon==None:
        return "Ingen stasjoner med dette navnet"
    if ukedag not in dager:
        return "Ikke en gyldig dag"
    
    ukedag_kode=dager.index(ukedag)

    con2 = sqlite3.connect("prosjektdatabase.db")
    cursor2 = con2.cursor()
    cursor2.execute("""SELECT RuteID 
                      FROM TogruteForekomst 
                      WHERE Dag = ? 
                      AND RuteID IN 
                      (SELECT RuteID 
                       FROM StasjonIRute 
                       WHERE StasjonNavn = ?)""",
                       (ukedag_kode,stasjonnavn,))

    output=cursor2.fetchall()
    #Man får ut tupler, må gjøre om til en liste med int
    alle_togruter_innom_stasjon = [x[0] for x in output]
    if len(alle_togruter_innom_stasjon)==0:
        print("Denne stasjonen har ingen togruter denne dagen")
    else:
        print("Alle togruter innon "+ stasjonnavn)
        for ruteID in alle_togruter_innom_stasjon:
            print("ruteID: ",ruteID)
    con2.close()


#alle_togruter_innom_stasjon()



