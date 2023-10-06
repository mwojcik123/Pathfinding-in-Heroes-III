USE [BD2024_z_1A]
GO
/*
02.01. Wyświetlić aktualną datę (bez czasu!).
*/
SELECT GETDATE() data;
/*
02.02. Wyświetlić napis "SELECT * FROM tabela;"
*/
SELECT 'SELECT * FROM tabela;';
/*
02.03. Wyświetlić wartości poszczególnych pozycji zamówień (tabela PozycjeZamówienia)
*/
SELECT *  FROM PozycjeZamówienia;
/*
02.04. Wyświetlić numer zamówienia, na którym występuje największa wartość pozycji zamówienia (tabela PozycjeZamówienia).
*/
SELECT TOP 1 IDzamówienia, CenaJednostkowa * Ilość wartosc FROM PozycjeZamówienia ORDER BY wartosc DESC;
/*
02.05. Wyświetlić aktualny wiek pracowników (w latach). Dane posortować rosnąco wg wieku i wyświetlić w formacie: Pracownik, Wiek.
*/
SELECT CONCAT(Imię, ' ', Nazwisko) pracownik, DATEDIFF(YEAR, DataUrodzenia, GETDATE()) wiek FROM Pracownicy ORDER BY wiek;
/*
02.06. Wyświetlić obwód koła o promieniu równym 1m.
*/
SELECT 2 * 1 * PI() pole;
/*
02.07. Wyświetlić dane adresowe dostawców w formie jednokolumnowej listy w formacie: Dostawca (adres pocztowy dostawcy).
*/
SELECT CONCAT(NazwaFirmy, ' (', Adres, ')')
FROM Dostawcy;
/*
02.08. Wyświetlić wartość wyrażenia Pi()/4.
*/
SELECT  PI() / 4;
/*
02.09. Wyświetlić dostawców z Polski lub ze Szwecji.
*/
SELECT * FROM Dostawcy WHERE Kraj = 'Polska' OR Kraj = 'Szwecja';
/*
02.10. Wyświetlić listę firm posiadających telefon, ale nie posiadających faksu.
*/
SELECT *
FROM Dostawcy
WHERE Telefon IS NOT NULL AND Faks IS NULL;
/*
02.11. Wyświetlić produkty należące do kategorii o identyfikatorze 6, których dostawcami są firmy o identyfikatorach 1, 2, 4, 5 i 9. 
*/
SELECT * FROM Produkty WHERE IDkategorii = 6 AND IDdostawcy IN (1, 2, 4, 5, 9)
/*
02.12. Wyświetlić produkty wycofane ze sprzedaży, które jeszcze zalegają w magazynie.
*/
SELECT *
FROM Produkty
WHERE Wycofany = 1 AND StanMagazynu > 0;
/*
02.13. Wyświetlić produkty będące aktualnie w ofercie sprzedaży, których brakuje w magazynie.
*/
SELECT *
FROM Produkty 
WHERE Wycofany = 0 AND StanMagazynu = 0;
/*
02.14. Wyświetlić produkty z kategorii o identyfikatorze 3, których cena jednostkowa jest mniejsza lub równa 15,98 zł. Dane pochodzą z tabeli Produkty.
*/
SELECT *
FROM Produkty 
WHERE IDkategorii = 3 AND CenaJednostkowa <= 15.99;
/*
02.15. Wyświetlić zamówienia zrealizowane w I kwartale 2014 roku. Dane pochodzą z tabeli Zamówienia.
*/
SELECT *
FROM Zamówienia
WHERE DataZamówienia >= '2014-01-01' AND DataZamówienia <= '2014-03-31';
/*
02.16. Wyświetlić zamówienia, które wysłano po wymaganym terminie.
*/
SELECT *
FROM Zamówienia
WHERE DataWysyłki > DataWymagana;