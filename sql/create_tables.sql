CREATE TABLE restaurants (
    id BIGINT PRIMARY KEY,
    name TEXT,
    cuisine TEXT,
    amenity TEXT,
    housenumber TEXT,
    street TEXT,
    city TEXT,
    lat NUMERIC(9,6),
    lon NUMERIC(9,6),
    phone TEXT
);
