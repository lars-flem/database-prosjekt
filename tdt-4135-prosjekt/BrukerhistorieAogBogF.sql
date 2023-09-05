INSERT INTO JernbaneStasjon (StasjonNavn, Moh)
VALUES 
    ("Trondheim S", 5.1),
    ("Steinkjer", 3.6),
    ("Mosjøen", 6.8),
    ("Mo i Rana", 3.5),
    ("Fauske", 34.0),
    ("Bodø", 4.1);

INSERT INTO Banestrekning (BaneID, Navn, Fremdriftsenergi, StartStasjon,SluttStasjon)
VALUES
    (1, "Nordlandsbanen", "Diesel", "Trondheim S", "Bodø");

INSERT INTO Delstrekning (DelStrekID, Lengde, Sportype, StartStasjon, SluttStasjon, BaneID)
VALUES
    (1, 120, "Dobbel", "Trondheim S", "Steinkjer", 1),
    (2, 280, "Enkel", "Steinkjer", "Mosjøen", 1),
    (3, 90, "Enkel", "Mosjøen", "Mo i Rana", 1),
    (4, 170, "Enkel", "Mo i Rana", "Fauske", 1),
    (5, 60, "Enkel", "Fauske", "Bodø", 1);

INSERT INTO Togrute (RuteID, MedRetningen, StartStasjon, SluttStasjon)
VALUES
    (1, "True", "Trondheim S", "Bodø"),
    (2, "True", "Trondheim S", "Bodø"),
    (3, "False", "Mo i Rana", "Trondheim S");

INSERT INTO StasjonIRute (StasjonNavn, RuteID, Ankomst, Avgang, StasjonNr)
VALUES
	("Trondheim S", 1, '07:49', '07:49', 1),
	("Steinkjer", 1, '09:51', '09:51', 2),
	("Mosjøen", 1, '13:20', '13:20', 3),
	("Mo i Rana", 1, '14:31', '14:31', 4),
	("Fauske", 1, '16:49', '16:49', 5),
	("Bodø", 1, '17:34', '17:34', 6),
	("Trondheim S", 2, '23:05', '23:05', 1),
	("Steinkjer", 2, '00:57', '00:57', 2),
	("Mosjøen", 2, '04:41', '04:41', 3),
	("Mo i Rana", 2, '05:55', '05:55', 4),
	("Fauske", 2, '08:19', '08:19', 5),
	("Bodø", 2, '09:05', '09:05', 6),
	("Mo i Rana", 3, '08:11', '08:11', 1),
	("Mosjøen", 3, '09:14', '09:14', 2),
	("Steinkjer", 3, '12:31', '12:31', 3),
	("Trondheim S", 3, '14:13', '14:13', 4);

INSERT INTO Sovevogn (RegNr, Navn, AntallSovekupeer, AntallSenger)
VALUES
    (5, "SJ-sovevogn-1", 4, 8);
    

INSERT INTO Sittevogn (RegNr, Navn, AntallStolRader, AntallSeterPerRad)
VALUES
    (1, "SJ-sittevogn-1", 3, 4),
    (2, "SJ-sittevogn-1", 3, 4),
    (3, "SJ-sittevogn-1", 3, 4),
    (4, "SJ-sittevogn-1", 3, 4);

INSERT INTO Vognoppsett (SittevognRegNr, SovevognRegNr, RuteID, VognNr)
VALUES
    (1,NULL,1,1), (2,NULL,1,2),(3,NULL,2,1), (NULL,5,2,2), (4,NULL,3,1);

INSERT INTO Seng (RegNr, PlassNr)
VALUES
    (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8);

INSERT INTO Sete (RegNr, PlassNr)
VALUES 
    (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9), (1,10), (1,11), (1,12),
    (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9), (2,10), (2,11), (2,12),
    (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7), (3,8), (3,9), (3,10), (3,11), (3,12),
    (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7), (4,8), (4,9), (4,10), (4,11), (4,12);

INSERT INTO TogruteForekomst (RuteID, Dato, Dag)
VALUES
    (1,"2023-04-03",0), (1,"2023-04-04",1),
    (2,"2023-04-03",0), (2,"2023-04-04",1),
    (3,"2023-04-03",0), (3,"2023-04-04",1);

INSERT INTO Operator (OperatorNavn)
VALUES ("SJ");

INSERT INTO OperererPaa (RuteID, OperatorNavn)
VALUES
    (1, "SJ"),(2, "SJ"),(3, "SJ");

INSERT INTO Kunde (KundeNr, Navn, Epost, MobilNr)
VALUES
    (1, "Ola Normann", "ola@mail.no", 12345678);

INSERT INTO KundeBase (KundeNr, OperatorNavn)
VALUES
    (1, "SJ");