from models import *
from flask import make_response, abort
import json

# GET api/routes
def list_routes(limit=25, offset=0):

    #Ensure limit > 0 but < 25
    check_for_limit(limit)

    query = Routes.select().limit(limit).offset(offset)

    routes = []
    for route in query:
        routes.append({"route_id": route.route_id, "route_nickname": route.route_nickname})

    return {"routes": routes}

# GET api/routes/{route_id}
def get_route(route_id):
    query = Routes.select().where(Routes.route_id == route_id)

    if query.count() == 0:
        abort(404, "Route not found")
    res = {}
    for data in query:
        res = {"route_id": data.route_id, "route_nickname": data.route_nickname}

    return res

# GET api/routes/{route_id}/trips
def list_routes_trips(route_id, limit=25, offset=0):

    #Ensure limit > 0 but < 25
    check_for_limit(limit)

    query = Trips.select().where(Trips.route_id == route_id).limit(limit).offset(offset)

    if query.count() == 0:
        abort(404, "Route not found")

    trips = []
    for trip in query:
        trips.append({"trip_id": trip.trip_id, "route_id": trip.route_id, "trip_headsign": trip.trip_headsign})

    return {"trips": trips}

# GET api/routes/{route_id}/trips/{trip_id}/stops
def list_trip_stops(route_id, trip_id, limit=25, offset=0):
    
    #Ensure limit > 0 but < 25
    check_for_limit(limit)

    query = (Stop_Times
        .select(Stop_Times, Stops, Trips)
        .join(Stops, on=(Stop_Times.stop_id == Stops.stop_id).alias('stop'))
        .switch(Stop_Times)
        .join(Trips, on=(Stop_Times.trip_id == Trips.trip_id).alias('trip'))
        .where(Stop_Times.trip_id == trip_id, Trips.route_id == route_id).limit(limit).offset(offset))

    if query.count() == 0:
        abort(404, "Trip not found")    

    stops = []
    for stop in query:
        stops.append({
            "trip_id": stop.trip_id,
            "arrival_time": stop.arrival_time,
            "departure_time": stop.departure_time,
            "stop_id": stop.stop.stop_id,
            "stop_name": stop.stop.stop_name,
            "trip_headsign": stop.trip.trip_headsign
        })
    
    return {"stops": stops}

#Error handling
def check_for_limit(limit):
    if limit == 0:
        abort(400, "Limit must be greater than 0")
    elif limit > 25:
        abort(400, "Limit cannot be greater than 25")