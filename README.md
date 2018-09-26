# Cat Bus API 🚌

![Cat Bus](app/static/img/catbus.gif)

Simple API wrapper for Austin's Capmetro GTFS data.

## Stack

1. Python 3
1. Docker handles standing up the MySQL database and Flask app
1. Flask server handles API requests
1. Swagger defines API and provides a UI for exploring the API
1. PeeWee is a lightweight Python ORM I used to make it easier to model and query data
1. Pandas is a package for Python I like using for manipulating CSV data

## Set up

This API requires [Docker](https://www.docker.com) to run locally.

1. `docker-compose build && docker-compose up` to build and bring up the project.
1. From the root directory, `pip install -r requirements.txt`. This pretty much only installs Pandas and PeeWee, which is needed to backfill data in the MySQL database.
1. Run the backfill: `python backfill.py`. Note: Backfilling stops, routes, and trips is pretty fast, but stop times will take a while. Drink some tea. 🍵

## Run the server

The API server is a Flask app that uses the Swagger spec. Using `docker-compose up` should bring up both the database and the Flask app.

1. The Flask app and API should be running on [localhost:5000](http://localhost:5000)
1. You should be able to curl the API on `http://localhost:5000/api` or use an app like [POSTMAN](https://www.getpostman.com/), or the Swagger UI link below.

## Swagger

![Swagger UI](app/static/img/swagger-ui.png)

Go to [http://localhost:5000/api/ui/](http://localhost:5000/api/ui/) on  your browser to check out the spec and make test calls!

## Challenges / To Do's

I was using MySQL version 8, but I had some compatibility issues being able to connect Flask to the MySQL 8 version of the DB due to how MySQL hashes passwords now. Articles I found online suggested downgrading to MySQL 5.

To Do's:

* [ ] Find workaround for MySQL 8 pw bug
* [ ] Set env var for db pw on container

## Database design and queries

### Design

I tried to mimick the [GTFS txt files](https://developers.google.com/transit/gtfs/) as much as possible in my database, and I made some decisions I probably wouldn't have made with what I know now, but I've gone too far :)

!["gone too far gif"](https://i.gifer.com/FbAt.gif)

For example, when I wrote my SQL schema, I decided to name route IDs as `route_id` everywhere, even in the routes table. This means that now I have `routes.route_id` instead of `routes.id`. I made that decision to remain consistent with the nomenclature of the txt files, but in retrospect, I would change that in the future to the more standard SQL practice of `table.id`.

### Queries

I thought it would be good to document the ORM + SQL queries for comparison purposes. Doing the join was much easier to do in MySQL than in PeeWee, so I hope this helps anyone looking for examples.

#### List routes

Routes.select().limit(LIMIT).offset(OFFSET)

MYSQL:

```
select * from routes limit X OFFSET X
```

#### Get a route

Routes.select().where(Routes.route_id == ID)

MYSQL:

```
select * from routes where route_id = ID
```

#### List all trips for a route

Trips.select().where(Trips.route_id == ID)

MYSQL:

```
select * from trips where route_id = ID
```

#### List stops by trip ID

This was tricker to do in the ORM than in pure SQL!

```
(Stop_Times
        .select(Stop_Times, Stops, Trips)
        .join(Stops, on=(Stop_Times.stop_id == Stops.stop_id).alias('stop'))
        .switch(Stop_Times)
        .join(Trips, on=(Stop_Times.trip_id == Trips.trip_id).alias('trip'))
        .where(Stop_Times.trip_id == trip_id, Trips.route_id == route_id).limit(limit).offset(offset))
```

MYSQL:

```
select arrival_time, departure_time, stops.stop_id, stops.stop_name, stop_times.trip_id, trips.trip_headsign 
from stop_times 
inner join stops on stop_times.stop_id = stops.stop_id 
inner join trips on stop_times.trip_id = trips.trip_id  
where stop_times.trip_id = ID;
```
