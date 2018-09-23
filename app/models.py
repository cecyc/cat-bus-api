from peewee import *
from playhouse.db_url import connect

#Models
#Usually I would set up the pwd as an env var, but for the sake of example...
db = connect('mysql://root@db:3306/bus_data')

class BaseModel(Model):
    class Meta:
        database = db

class Routes(BaseModel):
    route_id = SmallIntegerField(primary_key=True)
    route_nickname = CharField()

class Stops(BaseModel):
    stop_id = SmallIntegerField(primary_key=True)
    stop_code = SmallIntegerField()
    stop_name = CharField()

class Stop_Times(BaseModel):
    trip_id = IntegerField()
    arrival_time = CharField()
    departure_time = CharField()
    stop_id = SmallIntegerField()

class Trips(BaseModel):
    trip_id = IntegerField(primary_key=True)
    route_id = SmallIntegerField()
    trip_headsign = CharField()
    service_id  = CharField()

class Services(BaseModel):
    service_id  = CharField(primary_key=True)
    service_name = CharField()