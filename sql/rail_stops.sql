CREATE TABLE rail_stops (
    stop_id INTEGER NOT NULL PRIMARY KEY,
    stop_code INTEGER NOT NULL,
    stop_name TEXT,
    stop_desc TEXT,
    stop_lat DOUBLE PRECISION,
    stop_lon DOUBLE PRECISION,
    zone_id INTEGER
);
