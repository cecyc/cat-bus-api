USE bus_data;

CREATE TABLE routes (
  route_id int(4) UNSIGNED NOT NULL,
  route_nickname varchar(255),
  PRIMARY KEY (route_id)
);

CREATE TABLE stops (
  stop_id smallint(4) UNSIGNED NOT NULL,
  stop_code smallint(4) UNSIGNED NOT NULL,
  stop_name varchar(255),
  PRIMARY KEY (stop_id)
);

CREATE TABLE stop_times (
  id bigint(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  trip_id int(7) UNSIGNED NOT NULL,
  arrival_time varchar(255) NOT NULL,
  departure_time varchar(255) NOT NULL,
  stop_id smallint(4) UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY (id)
);

CREATE TABLE trips (
  trip_id int(7) UNSIGNED NOT NULL,
  route_id int(4) UNSIGNED NOT NULL,
  trip_headsign varchar(255),
  service_id varchar(255) NOT NULL,
  PRIMARY KEY (trip_id)
);

CREATE TABLE services (
  service_id varchar(255) NOT NULL,
  service_name varchar(255) NOT NULL,
  PRIMARY KEY (service_id)
);