import copy
from shutil import copyfile

import pandas as pd
import numpy as np
import random as rand
from faker import Faker
import datetime
import os
import csv
from dateutil.relativedelta import relativedelta
from faker_vehicle import VehicleProvider
from car import Car


#------------------------------------------------
#UTILITY FUNCTIONS:


def make_price(rounder, min, max):
    p = rand.uniform(min, max)
    p = p - (p % rounder)
    return p


def createCSV(fields, filename):
    with open(filename, 'w', newline="") as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)

def updateCSV(rows, filename):
    with open(filename, 'a', newline='') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(rows)

def process_cars():
    ids = pd.read_csv("cars_EXCEL_data_t1", usecols=["ID"])["ID"].tolist()
    makes = pd.read_csv("cars_EXCEL_data_t1", usecols=["Marka"])["Marka"].tolist()
    models = pd.read_csv("cars_EXCEL_data_t1", usecols=["Model"])["Model"].tolist()
    registers = pd.read_csv("cars_EXCEL_data_t1", usecols=["Rejestracja"])["Rejestracja"].tolist()
    vins = pd.read_csv("cars_EXCEL_data_t1", usecols=["Nr_VIN"])["Nr_VIN"].tolist()
    years = pd.read_csv("cars_EXCEL_data_t1", usecols=["Rocznik"])["Rocznik"].tolist()
    engines = pd.read_csv("cars_EXCEL_data_t1", usecols=["Silnik"])["Silnik"].tolist()
    bought_dates = pd.read_csv("cars_EXCEL_data_t1", usecols=["Data_zakupu"])["Data_zakupu"].tolist()
    start_kms = pd.read_csv("cars_EXCEL_data_t1", usecols=["Licznik_poczatkowy"])["Licznik_poczatkowy"].tolist()
    current_kms = pd.read_csv("cars_EXCEL_data_t1", usecols=["Licznik_obecny"])["Licznik_obecny"].tolist()
    last_check_dates = pd.read_csv("cars_EXCEL_data_t1", usecols=["Data_ostatniego_przegladu"])["Data_ostatniego_przegladu"].tolist()
    if_accident = pd.read_csv("cars_EXCEL_data_t1", usecols=["Czy_powypadkowy"])["Czy_powypadkowy"].tolist()
    last_trips = pd.read_csv("cars_EXCEL_data_t1", usecols=["Ostatnia trasa"])["Ostatnia trasa"].tolist()

    res = []
    for i in range(len(ids)):
        tmp_id = int(ids[i])
        tmp_make = makes[i]
        tmp_model = models[i]
        tmp_register = registers[i]
        tmp_vin = vins[i]
        tmp_year = int(years[i])
        tmp_engine = engines[i]
        y, m, d = bought_dates[i].split('-')
        tmp_bought_date = datetime.datetime(int(y), int(m), int(d))
        tmp_start_km = float(start_kms[i])
        tmp_current_km = float(current_kms[i])
        y, m, d = last_check_dates[i].split('-')
        tmp_last_check_date = datetime.datetime(int(y), int(m), int(d))
        tmp_if_accident = int(if_accident[i])
        tmp_last_trip = float(last_trips[i])
        res.append(Car(tmp_id, tmp_vin, tmp_register, tmp_year, tmp_make, tmp_model, tmp_engine, tmp_bought_date, tmp_start_km, tmp_last_check_date, tmp_current_km, tmp_if_accident, tmp_last_trip))
    return res

#------------------------------------------------
#INITIALIZING DATA:


# create some fake object
fake = Faker()
fake.add_provider(VehicleProvider)
fakePL = Faker("pl_PL")
start = None
end = None
delta_t = 0
if (os.path.isfile('./orders_data_t1')):
    delta_t = 2
else:
    delta_t = 1

#opcja 1 okresu czasu, pierwszego ładowania - tworzenie struktur danych i plikow docelowych
if delta_t == 1:
    createCSV(["Imie", "Nazwisko", "Nr_telefonu", "PESEL"], "clients_data_t1")
    createCSV(["Imie", "Nazwisko", "PESEL", "Pensja"], "workers_data_t1")
    createCSV(["ID_Skarga", "Tresc", "Data_zlozenia"], "complaints_data_t1")
    createCSV(["Nr_vin", "Marka", "Model", "Rocznik"], "cars_DB_data_t1")
    createCSV(["ID_Naprawa", "Data_rozpoczecia", "Data_zakonczenia", "Opis", "Koszt", "Samochod_VIN"], "repairs_data_t1")
    createCSV(["ID_Zlecenie", "Data_rozpoczecia", "Data_zakonczenia", "Wartosc", "Klient_PESEL", "Samochod_VIN", "Mechanik_PESEL"], "orders_data_t1")
    createCSV(["ID", "Marka", "Model", "Nr_VIN", "Rejestracja", "Rocznik", "Silnik", "Data_zakupu", "Licznik_poczatkowy",
               "Licznik_obecny", "Data_ostatniego_przegladu", "Czy_powypadkowy", "Ostatnia trasa"
               ], "cars_EXCEL_data_t1")

    #ustawiamy czas od-do do generacji:
    start = datetime.date(2010, 1, 1) #y, m, d
    end = datetime.date(2014, 12, 31)

    #przygotowujemy temp global variables
    cars_info = []  # informacje o wszystkich autach w liście
    c_len = 0 # długość listy aut (ilosc aut)
    fk_mech = []
    fkm_len = len(fk_mech) #ilosc mechanikow
    fk_cli =  [] # lista foreign keys klientow (pesele)
    fkc_len = len(fk_cli) #ilosc klientow
    orders_count = 0 # ilosc zamowien
    orders_temp = [] # tablica na przechowywanie zamowien z 1 miesiaca
    complaints_count = 0 # ilosc skarg
    complaints_temp = [] # tablica na przechowywanie skarg z 1 miesiaca
    last_called_client = 0 # ostatnio przypisany klient - potrzebne do zapewniania ze kazdy klient ma choc 1 zamowienie
    rep_counter = 0

elif delta_t == 2:
    fk_cli = pd.read_csv("clients_data_t1", usecols=["PESEL"])["PESEL"].tolist()
    fk_mech = pd.read_csv("workers_data_t1", usecols=["PESEL"])["PESEL"].tolist()
    fkm_len = len(fk_mech)
    fkc_len = len(fk_cli)
    orders_count = pd.read_csv("orders_data_t1", usecols=["ID_Zlecenie"])["ID_Zlecenie"].size
    orders_temp = []
    complaints_count = pd.read_csv("complaints_data_t1", usecols=["ID_Skarga"])["ID_Skarga"].size
    complaints_temp = []
    last_called_client = fkc_len
    c_len = 0
    start = datetime.date(2015, 1, 1) #y, m, d
    end = datetime.date(2020, 12, 31)
    cars_info = process_cars()
    rep_counter = len(pd.read_csv("repairs_data_t1", usecols=["ID_Naprawa"])["ID_Naprawa"].tolist())

    copyfile("clients_data_t1", "clients_data_t2")
    copyfile("complaints_data_t1", "complaints_data_t2")
    copyfile("orders_data_t1", "orders_data_t2")
    copyfile("repairs_data_t1", "repairs_data_t2")
    copyfile("workers_data_t1", "workers_data_t2")

    # os.remove("cars_DB_data")
    # os.remove("cars_EXCEL_data")
    createCSV(["Nr_vin", "Marka", "Model", "Rocznik"], "cars_DB_data_t2")
    createCSV(["ID", "Marka", "Model", "Nr_VIN", "Rejestracja", "Rocznik", "Silnik", "Data_zakupu", "Licznik_poczatkowy",
               "Licznik_obecny", "Data_ostatniego_przegladu", "Czy_powypadkowy", "Ostatnia trasa"
               ], "cars_EXCEL_data_t2")


def create_repairs_for_month(current_date):
    global rep_counter
    CHANCE = 0.1
    rep = []
    for car in cars_info:
        r = rand.randint(0, 100)
        if r <= CHANCE:
            days = rand.randint(0, 19)
            start_date = copy.copy(current_date)
            start_date += datetime.timedelta(days=days)
            days = rand.randint(0, 9)
            end_date = start_date + datetime.timedelta(days=days)
            tmp = [
                rep_counter + 1,
                str(start_date.year) + '-' + str(start_date.month) + '-' + str(start_date.day),
                str(end_date.year) + '-' + str(end_date.month) + '-' + str(end_date.day),
                fake.text(max_nb_chars=100),
                round(rand.uniform(100, 3000), 2),
                car.vin
            ]
            rep_counter += 1
            rep.append(tmp)
    if delta_t == 1:
        updateCSV(rep, "repairs_data_t1")
    else:
        updateCSV(rep, "repairs_data_t2")
    return rep


#------------------------------------------------
#GENERATION ITERATOR:


def begin_generating(start, end, regs):
    months = (end.year - start.year) * 12 + end.month - start.month
    for newmonth in range(1, months+1):
        start = start + relativedelta(months=1)
        print(start)
        generate_new_cars(start, rand.randint(33, 60), regs)
        create_repairs_for_month(start)
        generate_orders(start, rand.randint(35, 55))


#------------------------------------------------
#ENTITY GENERATING FUNCTIONS:
def pesels_from_file():
    part1 = pd.read_csv("clients_data_t1", usecols=["PESEL"])["PESEL"].tolist()
    part2 = pd.read_csv("workers_data_t1", usecols=["PESEL"])["PESEL"].tolist()
    res = []
    res.extend(part1)
    res.extend(part2)
    return res

def generate_pesels(*args):
    if len(args) == 1:
        return generate_pesels1(args[0])
    else:
        return generate_pesels2(args[0], args[1])

def generate_pesels1(num):
    x = set()
    while len(x) < num:
        x.add(fakePL.pesel())
        print("p: ", len(x))
    return list(x)


def generate_pesels2(num, pesels):
    x = set()
    for a in pesels:
        x.add(a)
    while len(x) < num + len(pesels):
            x.add(fakePL.pesel())
    for b in pesels:
        x.remove(b)
    res = list(x)
    return res


def generate_registrations(num):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    res = set()
    while len(res) < num:
        f1 = rand.choice(letters)
        f2 = rand.choice(letters)
        f3 = rand.choice(letters)

        s1 = rand.choice(numbers)
        s2 = rand.choice(numbers)
        s3 = rand.choice(letters)
        s4 = rand.choice(letters)

        tmp = f1 + f2 + f3 + ' ' + s1 + s2 + s3 + s4
        res.add(tmp)
    return list(res)


def generate_clients(pesels, num):
    global fk_cli
    global fkc_len
    res = []
    for i in range(num):
        p = rand.choice(pesels)
        pesels.remove(p)
        tmp = [fake.first_name(), fake.last_name(), fakePL.phone_number(), p]
        res.append(tmp)
        fk_cli.append(p)
        fkc_len += 1
        print("c: ", len(res))
    if delta_t == 1:
        updateCSV(res, "clients_data_t1")
    else:
        updateCSV(res, "clients_data_t2")


def generate_mechanics(pesels, num):
    global fk_mech
    global fkm_len
    res = []
    for i in range(num):
        p = rand.choice(pesels)
        pesels.remove(p)
        tmp = [fake.first_name(), fake.last_name(), p, round(rand.uniform(1500, 9500), 2)]
        res.append(tmp)
        fk_mech.append(p)
        fkm_len += 1
        print("m: ", len(res))
    if delta_t == 1:
        updateCSV(res, "workers_data_t1")
    else:
        updateCSV(res, "workers_data_t2")


def generate_new_cars(start, cars_bought, regs):
    global c_len
    global cars_info
    #tyle zakupiono w danym miesiacu
    for n in range(0, cars_bought):

        # id = 100000 + c_len + n
        id = c_len + n + 1
        # marka = "marka"
        # model = "model"
        # year = int(start.year)
        # rocznik = rand.randint(year - 10, year)
        #update globalnej listy o wygenerowane auto, bez csv bo to przechowujemy i tak w pamieci na ten moment
        # cars_info.append([id, marka, model, rocznik])
        cars_info.append(Car(start, id, regs, fake))
    #inkrementacja globalnego licznika aut w wypożyczalni
    c_len += cars_bought
    # updateCSV(orders_temp, "cars_DB_data")


def generate_orders(start, orders_made):
    global orders_temp
    global orders_count
    global fk_cli
    global fkc_len
    global last_called_client
    global fk_mech
    global fkm_len
    global c_len
    global cars_info
    global complaints_temp
    global complaints_count

    prawdopodobienstwo_skargi = 0.6

    chosen_cars = []
    max = start + relativedelta(months=1)

    for n in range(0, orders_made):
        #inkrementacja glob. licznika zamowien
        orders_count += 1

        #id na podstawie ogólnego numeru
        # id = 100000 + orders_count
        id = orders_count

        #losowanie dat
        data_pocz = fake.date_between(start_date=start, end_date=max)
        maxduration = max - data_pocz
        data_kon = data_pocz + datetime.timedelta(days=rand.randint(1, maxduration.days))
        wartosc = make_price(rounder=10, min=300, max=3000)

        #losowanie z klientem z zapewnieniem ze przynajmniej 1 zamowienie ma kazdy klient
        if orders_count>fkc_len:
            fk_klienta = fk_cli[rand.randint(0, fkc_len-1)]
        else:
            fk_klienta = fk_cli[last_called_client]
            last_called_client += 1

        #losowanie mechanika bez koniecznosci zapewnienia przynajmniej 1 zlecenia per mechanik
        fk_mechanika = fk_mech[(rand.randint(0, fkm_len-1))]

        #losowanie auta bez powtorzen w danym miesiacu
        auto = None
        match = False
        while match == False:
            # auto = cars_info[rand.randint(0,c_len-1)][0]
            auto = rand.choice(cars_info)
            if auto not in chosen_cars:
                chosen_cars.append(auto)
                match = True
        #UPDATE CAR INFO
        auto.update_after_trip(data_kon)
        #dodanie gotowego zamowienia do temp listy
        orders_temp.append([id, data_pocz, data_kon, wartosc, fk_klienta,auto.vin, fk_mechanika])

        if rand.random() < prawdopodobienstwo_skargi:
            complaints_temp.append([100000 + complaints_count, fake.text(max_nb_chars = 100), data_kon, id])
            complaints_count += 1
        print("order generated: " + str(id))

    if delta_t == 1:
        updateCSV(orders_temp, "orders_data_t1")
        updateCSV(complaints_temp, "complaints_data_t1")
    else:
        updateCSV(orders_temp, "orders_data_t2")
        updateCSV(complaints_temp, "complaints_data_t2")
    orders_temp = []
    complaints_temp = []

def search_by_vin(nr_vin):
    for e in cars_info:
        if e.vin == nr_vin:
            return e
    print("Not found")
    return None

if delta_t == 1:
    pesels = generate_pesels(10000)
else:
    pesels = generate_pesels(10000, pesels_from_file())
pesels = list(set(pesels))

if delta_t == 2:
    upd_vin = input("Podaj numer vin samochodu, którego rocznik zmienisz: ")
    upd = search_by_vin(upd_vin)
    if upd is not None:
        upd_year = int(input("Podaj nowy rocznik: "))
        upd.year = upd_year

generate_clients(pesels, 5000)
generate_mechanics(pesels, 5000)
regs = generate_registrations(10000)
generate_new_cars(start, 1000, regs)
begin_generating(start, end, regs)

cars_db = []
cars_excel = []
for a in cars_info:
    l1 = a.db_csv()
    cars_db.append(l1)
    l2 = a.excel_csv()
    cars_excel.append(l2)

if delta_t == 1:
    updateCSV(cars_db, "cars_DB_data_t1")
    updateCSV(cars_excel, "cars_EXCEL_data_t1")
else:
    updateCSV(cars_excel, "cars_EXCEL_data_t2")
    updateCSV(cars_db, "cars_DB_data_t2")