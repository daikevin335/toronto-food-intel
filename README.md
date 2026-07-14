# Toronto Food Intel 🍜

A personal data engineering project exploring Toronto's restaurant landscape — built by someone who has worked in kitchens, served customers, and genuinely loves food.

## Why I Built This

I've spent time working in the restaurant industry — from line cooking to front-of-house — and I've always been curious about the data side of food culture. Toronto is one of the most culinarily diverse cities in the world, and I wanted to use real data engineering tools to explore what that actually looks like on a map, by districts, and near transit.

This project was my way of combining a passion for food with hands-on practice in data extraction, SQL, and exploratory analysis.

## What I Found

- **Coffee shops dominate Toronto's food scene** — with 865 locations, they outnumber the next category (pizza, 681) by nearly 200
- **The downtown core is the densest food corridor** — St. Andrew station has 459 restaurants within ~500m, followed closely by Osgoode (445) and Queen (430)
- **Yonge Street leads by street** — 410 restaurants along its length, nearly double Bloor Street West (360)
- **Data completeness varies widely** — 98% of records have a name, but only 23% have a phone number, reflecting the volunteer-edited nature of OpenStreetMap

## Data Schema

    restaurants
    ├── id            BIGINT PRIMARY KEY
    ├── name          TEXT
    ├── cuisine       TEXT
    ├── amenity       TEXT
    ├── housenumber   TEXT
    ├── street        TEXT
    ├── city          TEXT
    ├── lat           NUMERIC(9,6)
    ├── lon           NUMERIC(9,6)
    └── phone         TEXT

    subway_stations
    ├── id            BIGINT PRIMARY KEY
    ├── name          TEXT
    ├── lat           NUMERIC(9,6)
    └── lon           NUMERIC(9,6)


## Key SQL Queries

**Restaurants within ~500m of each TTC subway station:**
```sql
SELECT 
    s.name as station,
    COUNT(*) as nearby_restaurants
FROM subway_stations s
JOIN restaurants r ON (
    ABS(r.lat - s.lat) < 0.005 AND
    ABS(r.lon - s.lon) < 0.007
)
GROUP BY s.name
ORDER BY nearby_restaurants DESC
LIMIT 10;
```

**Top cuisines across Toronto:**
```sql
SELECT cuisine, COUNT(*) as total
FROM restaurants
WHERE cuisine IS NOT NULL
GROUP BY cuisine
ORDER BY total DESC
LIMIT 10;
```

## Stack

- **Python** — data extraction and loading (`requests`, `psycopg2`, `pandas`)
- **PostgreSQL** — relational database storing 10,200+ restaurant and 68 TTC subway station records
- **OpenStreetMap Overpass API** — source of all restaurant and transit data
- **Jupyter Notebook** — exploratory analysis and visualizations
- **Git** — version control

## Project Structure

## Project Structure

    toronto-food-intel/
    ├── data/
    │   └── raw/
    │       ├── restaurants.json        # Raw OSM restaurant data
    │       └── subway_stations.json    # Raw TTC station data
    ├── notebooks/
    │   └── exploration.ipynb           # Analysis and visualizations
    ├── src/
    │   ├── extract.py                  # Pulls data from Overpass API
    │   ├── load.py                     # Loads restaurants into PostgreSQL
    │   └── load_subway.py              # Loads subway stations into PostgreSQL
    ├── sql/
    │   └── create_tables.sql           # Database schema
    └── requirements.txt


## How to Run It

### Prerequisites
- Python 3.x
- PostgreSQL (via Postgres.app on Mac)
- pip

### Setup

1. Clone the repo
```bash
git clone https://github.com/daikevin335/toronto-food-intel.git
cd toronto-food-intel
```

2. Install dependencies
```bash
pip3 install -r requirements.txt
```

3. Create the database in psql
```sql
CREATE DATABASE toronto_food_analytics;
\c toronto_food_analytics
```

4. Create the tables
```bash
psql toronto_food_analytics < sql/create_tables.sql
```

5. Extract data from OpenStreetMap
```bash
python3 src/extract.py
```

6. Load into PostgreSQL
```bash
python3 src/load.py
python3 src/load_subway.py
```

7. Open the notebook
```bash
jupyter notebook notebooks/exploration.ipynb
```

## Limitations & Next Steps

- **Proximity analysis uses a bounding box approximation** rather than true Haversine distance — good enough for exploration but not production-grade
- **OpenStreetMap data is volunteer-edited** — completeness varies significantly by field and location
- **Planned:** neighbourhood-level analysis, interactive map visualization, and Haversine-based distance calculations
