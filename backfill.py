import csv
import pandas
from peewee import *
from playhouse.db_url import connect

#Models
#Usually I would set up the pwd as an env var, but for the sake of example...
db = connect('mysql://root@0.0.0.0:3306/bus_data')

class BaseModel(Model):
    class Meta:
        database = db

class Routes(BaseModel):
    route_id = SmallIntegerField()
    route_nickname = CharField()

class Stops(BaseModel):
    stop_id = SmallIntegerField()
    stop_code = SmallIntegerField()
    stop_name = CharField()

class Stop_Times(BaseModel):
    trip_id = IntegerField()
    arrival_time = CharField()
    departure_time = CharField()
    stop_id = SmallIntegerField()

class Trips(BaseModel):
    trip_id = IntegerField()
    route_id = SmallIntegerField()
    trip_headsign = CharField()
    service_id  = CharField()

class Services(BaseModel):
    service_id  = CharField()
    service_name = CharField()

#CSVs to parse
stops = "capmetro/stops.csv"
stop_times = "capmetro/stop_times.csv"
trips = "capmetro/trips.csv"
routes = "capmetro/routes.csv"
services = "capmetro/calendar.csv"

# Do the backfill

print("Backfilling stops")
stops_df = pandas.read_csv(stops)

for i, row in stops_df.iterrows():
    Stops.create(stop_id = row[0], stop_code = row[1], stop_name = row[2])

print("Backfilling routes")
routes_df = pandas.read_csv(routes)

for i, row in routes_df.iterrows():
    Routes.create(route_id = row[0], route_nickname = row[3])

print("Backfilling services")
services_df = pandas.read_csv(services)

for i, row in services_df.iterrows():
    Services.create(service_id = row[0], service_name = row[-1])

print("Backfilling trips")
trips_df = pandas.read_csv(trips)

for i, row in trips_df.iterrows():
    Trips.create(trip_id = row[2], route_id = row[0], trip_headsign = row[3], service_id = row[1])

print("Backfilling stop times, this will take a while, go have a snack")
stop_times_df = pandas.read_csv(stop_times)

for i, row in stop_times_df.iterrows():
    Stop_Times.create(trip_id = row[0], arrival_time = row[1], departure_time = row[2], stop_id = row[3])

print("DONE! 🙌")