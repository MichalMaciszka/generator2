import random
from datetime import datetime

import vin

ACC_CHANCE = 0.4


class Car:
    def __init__(self, *args):
        if len(args) == 4:
            self.const1(
                args[0],
                args[1],
                args[2],
                args[3],
            )
        else:
            self.const2(
                args[0],
                args[1],
                args[2],
                args[3],
                args[4],
                args[5],
                args[6],
                args[7],
                args[8],
                args[9],
                args[10],
                args[11],
                args[12],
            )

    def const1(self, current_date, id, registrations, fake):
        self.id = id
        self.vin = vin.getRandomVin()
        self.registration = random.choice(registrations)
        registrations.remove(self.registration)
        t = fake.vehicle_year_make_model().split()
        self.year = int(t[0])
        self.make = t[1]
        self.model = t[2]
        if self.year > current_date.year:
            self.year = current_date.year - 1
        self.engine = str(round(random.uniform(1.0, 3.5), 1)) + ' ' + random.choice(['D', 'B'])
        self.bought_date = datetime(current_date.year, current_date.month, 1)
        self.start_km = random.randint(0, 300000)
        self.last_check_date = self.bought_date
        self.current_km = self.start_km
        self.if_accident = random.choice([0, 1])
        self.last_trip = 0

    def const2(self, id, vin, registration, year, make, model, engine, bought_date, start_km, last_check_date, current_km, if_accident, last_trip):
        self.id = id
        self. vin = vin
        self.registration = registration
        self.year = year
        self.make = make
        self.model = model
        self.engine = engine
        self.bought_date = bought_date
        self.start_km = start_km
        self.last_check_date = last_check_date
        self.current_km = current_km
        self.if_accident = if_accident
        self.last_trip = last_trip

    def update_after_trip(self, trip_end_date):
        self.last_check_date = trip_end_date
        self.last_trip = round(random.uniform(50, 5000), 2)
        self.current_km += self.last_trip

        if self.if_accident == 0:
            ch = random.uniform(0, 1)
            if ch < ACC_CHANCE:
                self.if_accident = 0
            else:
                self.if_accident = 1

    def to_sql(self):
        return {
            # 'ID': self.id,
            'VIN': self.vin,
            'Marka': self.make,
            'Model': self.model,
            'Rocznik': self.year
        }

    def to_excel(self):
        return {
            'ID': self.id,
            'Marka': self.make,
            'Model': self.model,
            'VIN': self.vin,
            'Nr_rejestracyjny': self.registration,
            'Rocznik': self.year,
            'Silnik': self.engine,
            'Data_zakupu': str(self.bought_date.year) + '-' + str(self.bought_date.month) + '-' + str(self.bought_date.day),
            'Licznik_poczatkowy': self.start_km,
            'Licznik_obecny': self.current_km,
            'Data_przegladu': str(self.last_check_date.year) + '-' + str(self.last_check_date.month) + '-' + str(self.last_check_date.day),
            'Ostatnia_podroz': self.last_trip
        }

    def db_csv(self):
        return [self.vin, self.make, self.model, self.year]

    def excel_csv(self):
        return [
            self.id, self.make, self.model, self.vin, self.registration, self.year,
            self.engine, (str(self.bought_date.year) + '-' + str(self.bought_date.month) + '-' + str(self.bought_date.day)),
            self.start_km, round(self.current_km, 2),
            (str(self.last_check_date.year) + '-' + str(self.last_check_date.month) + '-' + str(self.last_check_date.day)),
            self.if_accident, self.last_trip
                ]