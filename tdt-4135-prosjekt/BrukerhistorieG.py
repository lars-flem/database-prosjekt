import sqlite3
from datetime import datetime
from datetime import date


def main():
    con = sqlite3.connect("prosjektdatabase.db")
    cursor = con.cursor()
    def brukerHistorieG():
        print("Takk for at du vil reise med oss! Hvilken dato vil du reise?\n")
        billetkjop_Funk()
        
    def billetkjop_Funk():
            dato = input("Dato: \n")
            cursor.execute("""SELECT RuteID FROM TogruteForekomst WHERE Dato = ?""",(dato,))
            tilgjengeligeRuter = cursor.fetchall()
            if len(tilgjengeligeRuter) == 0:
                print("Det er dessverre ingen togruter den dagen\n")
                billetkjop_Funk()
            else:
                valgtRute = 0
                while(True):
                    visTilgjengeligeRuter(tilgjengeligeRuter)
                    valgtRute = input("Vennligst velg en av disse rutene, oppgi ruteID: ")
                    ruter = []
                    for each in tilgjengeligeRuter:
                        ruter.append(each[0])
                    if int(valgtRute) in ruter:
                        break
                    else:
                        print("Velg en gyldig RuteID")
                    print(ruter)
                cursor.execute("""SELECT StasjonNavn from StasjonIRute WHERE RuteID = ? ORDER BY StasjonNr""",(valgtRute))
                stasjoner_i_valgt_rute = cursor.fetchall()
                print("Stasjoner i ruten")
                cell_width = 15
                print("+{}+".format("-" * (cell_width + 2)))
                for j in stasjoner_i_valgt_rute:
                    print("| {:<{width}} |".format(j[0], width=cell_width))
                print("+{}+".format("-" * (cell_width + 2)))
                start = ""
                while(True):
                    start = input("Vennligst skriv på hvilken stasjon du vil gå på: ")
                    startStasjoner = []
                    for each in stasjoner_i_valgt_rute:
                        startStasjoner.append(each[0])
                    if start in startStasjoner:
                        break
                    else:
                        print("Vennligst velg en stasjon fra listen.")
                cursor.execute("""SELECT StasjonNr FROM StasjonIRute WHERE RuteID =? AND StasjonNavn = ?""",(valgtRute, start))
                startNr = cursor.fetchone()
                slutt = ""
                while(True):
                    slutt = input("Vennligst skriv på hvilken stasjon du vil av gå på: ")
                    sluttStasjoner = []
                    for each in stasjoner_i_valgt_rute:
                        sluttStasjoner.append(each[0])
                    if start in sluttStasjoner:
                        break
                    else:
                        print("Vennligst velg en stasjon fra listen.")
                cursor.execute("""SELECT StasjonNr FROM StasjonIRute WHERE RuteID =? AND StasjonNavn = ?""",(valgtRute,slutt))
                sluttNr = cursor.fetchone()
                cursor.execute("""SELECT MAX(OrdreNr) FROM KundeOrdre""")
                gammelID = cursor.fetchone()
                if gammelID[0] is None:
                    nyID=1
                else:
                    nyID = gammelID[0] + 1
                kundeEpost = input("Tusen takk, vennlist skriv din epost du er registrert med: ")
                cursor.execute("""SELECT KundeNr FROM Kunde WHERE Epost = ?""",(kundeEpost,))
                kundeNr = cursor.fetchone()
                cursor.execute("""SELECT * FROM Kundebase WHERE OperatorNavn = ? AND KundeNr = ?""",("SJ", kundeNr[0]))
                kundebaseFetch = cursor.fetchone()
                if kundebaseFetch == None:
                    cursor.execute("""INSERT INTO KundeBase VALUES (?,?)""",(kundeNr[0], "SJ"))
                    con.commit()
                #currentDate = date.today()
                currentDate='2023-04-01'
                #nowTime = Time = datetime.now()
                #currentTime = nowTime.strftime("%H:%M:%S")
                currentTime='12:00'
                cursor.execute("""INSERT INTO KundeOrdre (OrdreNr, DatoKjøpt, TidKjøpt, KundeNr, StartStasjon, SluttStasjon, Dato, RuteID) VALUES (?,?,?,?,?,?,?,?);""",(nyID, currentDate, currentTime, kundeNr[0], start, slutt, dato, valgtRute))
                con.commit()
                print("Her er alle tilgjengelige plasser: \n")
                cursor.execute("""SELECT SittevognRegNr, SovevognRegNr, VognNr FROM Vognoppsett WHERE RuteID = ?""",(valgtRute))
                vogner = cursor.fetchall()
                cursor.execute("""SELECT * FROM Billettkjop NATURAL JOIN KundeOrdre WHERE Dato = ? AND RuteID = ?""",(dato,valgtRute))
                reservasjoner = cursor.fetchall()
                plasserBooket = []
                for reservasjon in reservasjoner:
                    cursor.execute("""SELECT StasjonNr FROM StasjonIRute WHERE RuteID = ? AND StasjonNavn = ?""",(valgtRute, reservasjon[8]))
                    startRes = cursor.fetchone()
                    startRes2 = startRes[0]
                    cursor.execute("""SELECT StasjonNr FROM StasjonIRute WHERE RuteID = ? AND StasjonNavn = ?""",(valgtRute, reservasjon[9]))
                    sluttRes = cursor.fetchone()
                    sluttRes2 = sluttRes[0]
                    if startRes2 <= startNr[0] and sluttRes2 <= startNr[0]:
                        continue
                    elif startRes2 >= sluttNr[0] and sluttRes2 >= sluttNr[0]:
                        continue
                    else:
                        plasserBooket.append(reservasjon[0:5])

                visPlasser(vogner,plasserBooket)
                kjopBilett(nyID, start, slutt, dato, valgtRute, sjekkReservasjoner(startNr, sluttNr, dato, valgtRute), startNr, sluttNr, vogner)

    def visTilgjengeligeRuter(tilgjengeligeRuter):
        cell_width = 15
        header = ("RuteID", "Start", "Slutt")
        print("+{0}+{0}+{0}+"
            .format("-" * (cell_width + 2)))
        print("| {:<{width}} | {:<{width}} | {:<{width}} |"
            .format(header[0], header[1], header[2], width=cell_width))
        print("+{0}+{0}+{0}+"
            .format("-" * (cell_width + 2)))
        for i in tilgjengeligeRuter:
            cursor.execute("""SELECT StartStasjon, SluttStasjon FROM Togrute WHERE RuteID = ?""",(i))
            ruteS_S = cursor.fetchone()
            print("| {:<{width}} | {:<{width}} | {:<{width}} |"
                .format(i[0], ruteS_S[0], ruteS_S[1], width=cell_width))
            print("+{0}+{0}+{0}+"
                .format("-" * (cell_width + 2)))

    def sjekkReservasjoner(startNr, sluttNr, dato, valgtRute):
        cursor.execute("""SELECT * FROM Billettkjop NATURAL JOIN KundeOrdre WHERE Dato = ? AND RuteID = ?""",(dato,valgtRute))
        reservasjoner = cursor.fetchall()
        plasserBooket = []
        for reservasjon in reservasjoner:
            cursor.execute("""SELECT StasjonNr FROM StasjonIRute WHERE RuteID = ? AND StasjonNavn = ?""",(valgtRute, reservasjon[8]))
            startRes = cursor.fetchone()
            startRes2 = startRes[0]
            cursor.execute("""SELECT StasjonNr FROM StasjonIRute WHERE RuteID = ? AND StasjonNavn = ?""",(valgtRute, reservasjon[9]))
            sluttRes = cursor.fetchone()
            sluttRes2 = sluttRes[0]
            if startRes2 <= startNr[0] and sluttRes2 <= startNr[0]:
                continue
            elif startRes2 >= sluttNr[0] and sluttRes2 >= sluttNr[0]:
                continue
            else:
                plasserBooket.append(reservasjon[0:5])
        return plasserBooket
    
    def kjopBilett(nyID, start, slutt, dato, valgtRute, plasserBooket, startNr, sluttNr, vogner):
        valgtVogn = input("Vennligst velg hvilket vognnummer du vil sitte på: ")
        cursor.execute("""SELECT SittevognRegNr, SovevognRegNr FROM Vognoppsett WHERE VognNr = ? AND RuteID =?""",(valgtVogn, valgtRute))
        valgtRegNr = cursor.fetchone()
        plassErSete = 0
        if valgtRegNr[0] != None:
            plassErSete = 1
        valgtPlass = input("Vennligst velg hvilken plass du vil sitte på i vognen: ")
        opptatt = 0
        for booking in plasserBooket:
            if plassErSete==1:
                if booking[1] == int(valgtPlass) and booking[3] == int(valgtRegNr[0]):
                    opptatt = 1
                    
            else:
                if booking[2] == int(valgtPlass) and booking[4] == int(valgtRegNr[1]):
                    opptatt = 1
        if opptatt == 1:
            print("Vennligst velg en ledig plass\n") 
            kjopBilett(nyID, start, slutt, dato, valgtRute,sjekkReservasjoner(startNr, sluttNr, dato, valgtRute),startNr, sluttNr, vogner)
        else:   
            if plassErSete == 1:
                cursor.execute("""INSERT INTO Billettkjop VALUES (?, ?, NULL, ?, NULL);""",(nyID,valgtPlass,valgtRegNr[0]))
                con.commit()
            else:
                if int(valgtPlass)%2==0:
                    cursor.execute("""INSERT INTO Billettkjop VALUES (?, NULL, ?,NULL, ?);""",(nyID,int(valgtPlass),valgtRegNr[1]))
                    con.commit()
                    cursor.execute("""INSERT INTO Billettkjop VALUES (?, NULL, ?,NULL, ?);""",(nyID,int(valgtPlass)-1,valgtRegNr[1]))
                    con.commit()
                else:
                    cursor.execute("""INSERT INTO Billettkjop VALUES (?, NULL, ?,NULL, ?);""",(nyID,int(valgtPlass),valgtRegNr[1]))
                    con.commit()
                    cursor.execute("""INSERT INTO Billettkjop VALUES (?, NULL, ?,NULL, ?);""",(nyID,int(valgtPlass)+1,valgtRegNr[1]))
                    con.commit()
            bestille_Mer = input("Bestillingen er gjennomført, vil du reservere flere seter?(y/n)")
            if bestille_Mer == "y":
                visPlasser(vogner, sjekkReservasjoner(startNr, sluttNr, dato, valgtRute))
                kjopBilett(nyID, start, slutt, dato, valgtRute,sjekkReservasjoner(startNr, sluttNr, dato, valgtRute), startNr, sluttNr, vogner)
            elif bestille_Mer =="n":
                print("Takk for at du reiser med oss!")
    def visPlasser(vogner,plasserBooket):
        for x in range (0,len(vogner)):
                    if vogner[x][0] != None:
                        cursor.execute("""SELECT Navn from Sittevogn WHERE RegNr =?""",(vogner[x][0],))
                        sittevogn = cursor.fetchone()
                        
                        num_rows = 3
                        num_seats_per_row = 4
                        box_width = 14

                        
                        print("{:=^48}".format(""))
                        print("{:^48}".format(sittevogn[0] + " Vognnummer: " + str(vogner[x][2])))
                        print("{:=^48}".format(""))

                        
                        cursor.execute("""SELECT PlassNr FROM Sete WHERE RegNr = ?""", (vogner[x][0],))
                        plasser = cursor.fetchall()
                        booked_seats = [booking[1] for booking in plasserBooket if booking[3] == vogner[x][0]]

                   
                        print("|{:-^46}|".format(""))

                        
                        for row in range(num_rows):
                            
                            for seat in range(num_seats_per_row):
                                seat_num = row*num_seats_per_row + seat + 1
                               
                                if seat_num not in booked_seats:
                                    print("{:^11d}".format(seat_num), end="")
                                else:
                                    print("{:^11s}".format("X"), end="")
    
                            print("\n|{:-^46}|".format(""))
                        print("{:=^48}".format(""))

                    else:
                        cursor.execute("""SELECT Navn FROM Sovevogn WHERE RegNr =?""",(vogner[x][1],))
                        sovevogn = cursor.fetchone()
                        num_compartments = 4
                        num_beds_per_compartment = 2
                        box_width = 6
                        print("{:=^45}".format(""))
                        print("{:^45}".format(sovevogn[0] + " Vognnummer: " + str(vogner[x][2])))
                        print("{:=^45}".format(""))
                        cursor.execute("""SELECT PlassNr FROM Seng WHERE RegNr = ?""", (vogner[x][1],))
                        senger = cursor.fetchall()
                        booked_beds = [booking[2] for booking in plasserBooket if booking[4] == vogner[x][1]]
                        for compartment in range(num_compartments):
                            print("|{:^13}".format("Compartment " + str(compartment+1)), end="")
                            for bed in range(num_beds_per_compartment):
                                bed_num = compartment*num_beds_per_compartment + bed + 1
                                if bed_num not in booked_beds:
                                    print("|{:^6d}".format(bed_num), end="")
                                else:
                                    print("|{:^6s}".format("X"), end="")
                            print("|")
                            print("|" + "-"*box_width + "+" + "-"*box_width + "|")
                        print("|{:=^43}|".format(""))

            

    brukerHistorieG()
#main()
