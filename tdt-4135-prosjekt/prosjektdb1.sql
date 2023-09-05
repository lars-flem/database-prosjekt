DROP TABLE IF EXISTS Billettkjop;
DROP TABLE IF EXISTS KundeOrdre;
DROP TABLE IF EXISTS KundeBase;
DROP TABLE IF EXISTS Kunde;
DROP TABLE IF EXISTS OperererPaa;
DROP TABLE IF EXISTS Operator;
DROP TABLE IF EXISTS TogruteForekomst;
DROP TABLE IF EXISTS Sete;
DROP TABLE IF EXISTS Seng;
DROP TABLE IF EXISTS Vognoppsett;
DROP TABLE IF EXISTS Sittevogn;
DROP TABLE IF EXISTS Sovevogn;
DROP TABLE IF EXISTS StasjonIRute;
DROP TABLE IF EXISTS Togrute;
DROP TABLE IF EXISTS Delstrekning;
DROP TABLE IF EXISTS Banestrekning;
DROP TABLE IF EXISTS JernbaneStasjon;

CREATE TABLE JernbaneStasjon (
    StasjonNavn VARCHAR(50),
    Moh REAL NOT NULL,
    CONSTRAINT PK_JernbaneStasjon PRIMARY KEY (StasjonNavn)
);

CREATE TABLE Banestrekning (
    BaneID INT,
    Navn VARCHAR(50) NOT NULL,
    Fremdriftsenergi VARCHAR(50) NOT NULL,
    StartStasjon VARCHAR(50) NOT NULL,
    SluttStasjon VARCHAR(50) NOT NULL,
    CONSTRAINT PK_Banestrekning PRIMARY KEY (BaneID),
    CONSTRAINT FK_Banestrekning_StartStasjon_JernbaneStasjon FOREIGN KEY (StartStasjon) REFERENCES JernbaneStasjon(StasjonNavn) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Banestrekning_SluttStasjon_JernbaneStasjon FOREIGN KEY (SluttStasjon) REFERENCES JernbaneStasjon(StasjonNavn) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Delstrekning (
    DelStrekID INT,
    Lengde REAL NOT NULL,
    Sportype VARCHAR(50) NOT NULL,
    StartStasjon VARCHAR(50) NOT NULL,
    SluttStasjon VARCHAR(50) NOT NULL,
    BaneID INT NOT NULL,
	CONSTRAINT CHK_Type CHECK (Sportype = 'Enkel' OR Sportype = 'Dobbel'),
    CONSTRAINT PK_Delstrekning PRIMARY KEY (DelStrekID),
    CONSTRAINT FK_Delstrekning_StartStasjon_JernbaneStasjon FOREIGN KEY (StartStasjon) REFERENCES JernbaneStasjon(StasjonNavn) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Delstrekning_SluttStasjon_JernbaneStasjon FOREIGN KEY (SluttStasjon) REFERENCES JernbaneStasjon(StasjonNavn) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Delstrekning_BaneID_Banestrekning FOREIGN KEY (BaneID) REFERENCES Banestrekning(BaneID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Togrute (
    RuteID INT,
    MedRetningen VARCHAR(50) NOT NULL,
    StartStasjon VARCHAR(50) NOT NULL,
    SluttStasjon VARCHAR(50) NOT NULL,
    CONSTRAINT PK_Togrute PRIMARY KEY (RuteID),
	CONSTRAINT CHK_Retning CHECK (MedRetningen = 'True' OR MedRetningen = 'False'),
    CONSTRAINT FK_Togrute_StartStasjon_JernbaneStasjon FOREIGN KEY (StartStasjon) REFERENCES JernbaneStasjon(StasjonNavn) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Togrute_SluttStasjon_JernbaneStasjon FOREIGN KEY (SluttStasjon) REFERENCES JernbaneStasjon(StasjonNavn) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE StasjonIRute (
    StasjonNavn VARCHAR(50),
	RuteID INT,
	Ankomst TIME NOT NULL,
    Avgang TIME NOT NULL,
    StasjonNr INT NOT NULL,
	CONSTRAINT FK_StasjonIRute_StasjonNavn_Jerbanestasjon FOREIGN KEY (StasjonNavn) REFERENCES JernbaneStasjon(StasjonNavn) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT FK_StasjonIRute_RuteID_Togrute FOREIGN KEY (RuteID) REFERENCES Togrute(RuteID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT PK_StasjonIRute PRIMARY KEY (StasjonNavn, RuteID)
);

CREATE TABLE Sovevogn (
    RegNr INT,
    Navn VARCHAR(50) NOT NULL,
    AntallSovekupeer INT NOT NULL,
    AntallSenger INT NOT NULL,
	CONSTRAINT PK_Sovevogn PRIMARY KEY (RegNr)
);

CREATE TABLE Sittevogn (
    RegNr INT,
    Navn VARCHAR(50) NOT NULL,
    AntallStolRader INT NOT NULL,
    AntallSeterPerRad INT NOT NULL,
	CONSTRAINT PK_Sittevogn PRIMARY KEY (RegNr)
);
CREATE TABLE Vognoppsett (
SittevognRegNr INT,
SovevognRegNr INT,
RuteID INT,
VognNr INT,
CONSTRAINT FK_Vognoppsett_Sittevogn FOREIGN KEY (SittevognRegNr) REFERENCES Sittevogn(RegNr) ON DELETE CASCADE ON UPDATE CASCADE,
CONSTRAINT FK_Vognoppsett_Sovevogn FOREIGN KEY (SovevognRegNr) REFERENCES Sovevogn(RegNr) ON DELETE CASCADE ON UPDATE CASCADE,
CONSTRAINT FK_Vognoppsett_RuteID_Togrute FOREIGN KEY (RuteID) REFERENCES Togrute(RuteID) ON DELETE CASCADE ON UPDATE CASCADE,
CONSTRAINT PK_Vognoppsett PRIMARY KEY (SittevognRegNr, SovevognRegNr, RuteID)
);

CREATE TABLE Seng (
    RegNr INT,
    PlassNr INT,
	CONSTRAINT FK_Seng_RegNr_Sovevogn FOREIGN KEY (RegNr) REFERENCES Sovevogn(RegNr) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT PK_Seng PRIMARY KEY (RegNr, PlassNr)
);

CREATE TABLE Sete (
    RegNr INT,
    PlassNr INT,
	CONSTRAINT FK_Sete_RegNr_Sittevogn FOREIGN KEY (RegNr) REFERENCES Sittevogn(RegNr) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT PK_Sete PRIMARY KEY (RegNr, PlassNr)
);

CREATE TABLE TogruteForekomst (
    RuteID INT,
    Dato DATE,
    Dag INT NOT NULL,
	CONSTRAINT FK_TogruteForekomst_RuteId_Togrute FOREIGN KEY (RuteId) REFERENCES Togrute(RuteID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT PK_TogruteForekomst PRIMARY KEY (RuteID, Dato)
);

CREATE TABLE Operator (
    OperatorNavn VARCHAR(50),
	CONSTRAINT PK_Operator PRIMARY KEY (OperatorNavn)
);

CREATE TABLE OperererPaa (
    RuteID INT,
    OperatorNavn VARCHAR(50),
	CONSTRAINT FK_OpererPaa_RuteID_Togrute FOREIGN KEY (RuteID) REFERENCES Togrute(RuteID) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT FK_OpererPaa_OperatorNavn_Operator FOREIGN KEY (OperatorNavn) REFERENCES Operator(OperatorNavn) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT PK_OpererPaa PRIMARY KEY (RuteID, OperatorNavn)
);

CREATE TABLE Kunde (
	KundeNr INT,
	Navn VARCHAR(50) NOT NULL,
	Epost VARCHAR(50) NOT NULL UNIQUE,
	MobilNr int NOT NULL UNIQUE,
	CONSTRAINT PK_Kunde PRIMARY KEY (KundeNr)
);


CREATE TABLE KundeBase (
    KundeNr INT,
    OperatorNavn VARCHAR(50),
	CONSTRAINT FK_KundeBase_KundeNr_Kunde FOREIGN KEY (KundeNr) REFERENCES Kunde(KundeNr) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT FK_KundeBase_OperatorNavn_Operator FOREIGN KEY (OperatorNavn) REFERENCES Operator(OperatorNavn) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT PK_KundeBase PRIMARY KEY(KundeNr, OperatorNavn)
);

CREATE TABLE KundeOrdre(
	OrdreNr INT,
	DatoKjøpt DATE NOT NULL,
	TidKjøpt TIME NOT NULL,
	KundeNr INT NOT NULL,
	StartStasjon VARCHAR(50) NOT NULL,
    SluttStasjon VARCHAR(50) NOT NULL,
	Dato DATE NOT NULL,
	RuteID INT NOT NULL,
	CONSTRAINT PK_KundeOrdre PRIMARY KEY (OrdreNr),
	CONSTRAINT FK_KundeOrdre_KundeNr_Kunde FOREIGN KEY (KundeNr) REFERENCES Kunde(KundeNr) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT FK_KundeOrdre_StartStasjon_Jernbanestasjon FOREIGN KEY (StartStasjon) REFERENCES JernbaneStasjon(StasjonNavn) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT FK_KundeOrdre_SluttStasjon_Jernbanestasjon FOREIGN KEY (SluttStasjon) REFERENCES JernbaneStasjon(StasjonNavn) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT FK_KundeOrdre_Togrute FOREIGN KEY(Dato, RuteID) REFERENCES TogruteForekomst(Dato, RuteID)
);

CREATE TABLE Billettkjop (
	OrdreNr INT,
	SetePlassNr INT,
	SengPlassNr INT,
	SeteRegNr INT,
	SengRegNr INT,
	CONSTRAINT FK_Billetkjop_OrdreNr_KundeOrdre FOREIGN KEY (OrdreNr) REFERENCES KundeOrdre(OrdreNr) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT FK_Billetkjop_Sete FOREIGN KEY (SeteRegNr, SetePlassNr) REFERENCES Sete(RegNr,PlassNr) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT FK_Billetkjop_Seng FOREIGN KEY (SengRegNr, SengPlassNr) REFERENCES Seng(RegNr, PlassNr) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT PK_Billetkjop PRIMARY KEY (OrdreNr, SengPlassNr, SetePlassnr, SeteRegNr, SengRegNr)
	
);