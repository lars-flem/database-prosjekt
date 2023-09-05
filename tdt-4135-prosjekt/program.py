from BrukerhistorieC import alle_togruter_innom_stasjon
from BrukerhistorieH import vis_fremtidige_kjøp
from BrukerhistorieD import togrute_mellom_stasjoner
from BrukerhistorieE import register_kunde
from BrukerhistorieG import main
import sqlite3
import time



print("Hei, velkommen til Togruteprogrammet vårt!")
time.sleep(1.0)
print("Fyller den tomme databasen med data for brukerhistore A, B og F gjennom scipt...")


#Legger inn data i databasen
con = sqlite3.connect('prosjektdatabase.db')
with open('prosjektdb1.sql', 'r', encoding='utf-8') as sql_file:
    con.executescript(sql_file.read())
con.close()

con2 = sqlite3.connect('prosjektdatabase.db')
with open('BrukerhistorieAogBogF.sql', 'r', encoding='utf-8') as sql_file:
    con2.executescript(sql_file.read())
con2.close()

time.sleep(2.0)
print("Scriptet er lagt inn!")
time.sleep(1.0)
#Lar brukeren velge brukerhistorie
Kjøre=True
while Kjøre==True:
    print("""Her er alle brukerhistoriene:
          C) alle togruter som er innom stasjonen en gitt ukedag
          D) søke etter togruter som går mellom en startstasjon og en sluttstasjon
          E) registere deg som kunde
          G) finne ledige billetter for en oppgitt strekning på en ønsket togrute og kjøpe de billettene hen ønsker
          H) finne all informasjon om de kjøpene hen har gjort for fremtidige reiser 
          """)
    
    valg=input("Skriv bokstaven på historien du vil ha tilgang til: ")
    if valg=="C":
        alle_togruter_innom_stasjon()
    if valg=="D":
        togrute_mellom_stasjoner()
    if valg=="E":
        register_kunde()
    if valg=="G":
        main()
    if valg=="H":
        vis_fremtidige_kjøp()
        
    fortsette=input("Vil du fortsette programmet? y/n: ")
    if fortsette=="n":
        print('''
              
     ~~~          
   ~~   ____   |~~~~~~~~~~~~~~~|
  Y_,___|[]|   |   Choo Choo!  |
 {|_|_|_|DD|_,_|_______________|
//oo---OO=OO     OOO       OOO
              ''')
        Kjøre=False
    
    