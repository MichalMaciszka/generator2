/*CREATE DATABASE Wypozyczalnia4
GO*/

USE Wypozyczalnia4
GO


CREATE TABLE Klient
(
	Imie varchar(50),
	Nazwisko varchar(50),
	Nr_telefonu varchar(16),
	PESEL varchar(11) PRIMARY KEY
)

CREATE TABLE Samochod
(
	Nr_vin VARCHAR(17) PRIMARY KEY,
	Marka VARCHAR(30),
	Model VARCHAR(30),
	Rocznik INTEGER
)

CREATE TABLE Mechanik
(
	Imie VARCHAR(50),
	Nazwisko VARCHAR(50),
	PESEL VARCHAR(11) PRIMARY KEY,
	Pensja FLOAT
)

CREATE TABLE Naprawa
(
	ID_Naprawa INTEGER PRIMARY KEY,
	Data_rozpoczecia DATE,
	Data_zakonczenia DATE,
	Opis VARCHAR(300),
	Koszt FLOAT,
	Samochod_VIN VARCHAR(17) FOREIGN KEY REFERENCES Samochod
)

CREATE TABLE Zlecenie
(
	ID_Zlecenie INTEGER PRIMARY KEY,
	Data_rozpoczecia DATE,
	Data_zakonczenia DATE,
	Wartosc FLOAT,
	Klient_PESEL VARCHAR(11) NOT NULL FOREIGN KEY REFERENCES Klient,
	Samochod_VIN VARCHAR(17) FOREIGN KEY REFERENCES Samochod,
	Mechanik_PESEL VARCHAR(11) FOREIGN KEY REFERENCES Mechanik
)

CREATE TABLE Skarga
(
	ID_Skarga INTEGER PRIMARY KEY,
	Tresc VARCHAR(300),
	Data_zlozenia DATE,
	ID_Zlecenie INTEGER NOT NULL FOREIGN KEY REFERENCES Zlecenie
)