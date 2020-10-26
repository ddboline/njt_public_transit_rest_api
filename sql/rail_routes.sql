CREATE TABLE rail_routes (
    route_id INTEGER NOT NULL PRIMARY KEY,
    agency_id TEXT,
    route_short_name TEXT,
    route_long_name TEXT,
    route_type INTEGER,
    route_url TEXT,
    route_color TEXT
);