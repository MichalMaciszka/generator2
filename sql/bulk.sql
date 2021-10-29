use Wypozyczalnia4
GO

BULK INSERT dbo.Klient FROM 'D:\python\generator\clients_data_t2' WITH (FIELDTERMINATOR=',', FIRSTROW=2)

BULK INSERT dbo.Mechanik FROM 'D:\python\generator\workers_data_t2' WITH (FIELDTERMINATOR=',', FIRSTROW=2)

BULK INSERT dbo.Samochod FROM 'D:\python\generator\cars_DB_data_t2' WITH (FIELDTERMINATOR=',', FIRSTROW=2)

BULK INSERT dbo.Naprawa FROM 'D:\python\generator\repairs_data_t2' WITH (FIELDTERMINATOR=',', FIRSTROW=2)

BULK INSERT dbo.Zlecenie FROM 'D:\python\generator\orders_data_t2' WITH (FIELDTERMINATOR=',', FIRSTROW=2)

BULK INSERT dbo.Skarga FROM 'D:\python\generator\complaints_data_t2' WITH (FIELDTERMINATOR=',', FIRSTROW=2)