CREATE TABLE rail_trips (
    route_id INTEGER NOT NULL,
    service_id INTEGER,
    trip_id INTEGER NOT NULL PRIMARY KEY,
    trip_headsign TEXT,
    direction_id INTEGER,
    block_id TEXT,
    shape_id INTEGER
);