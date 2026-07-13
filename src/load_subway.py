import json
import psycopg2
from pathlib import Path

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="toronto_food_analytics",
    user="kevindai"
)
cursor = conn.cursor()

# Load subway station JSON
data = json.load(open('data/raw/subway_stations.json'))

for element in data['elements']:
    if 'lat' not in element or 'lon' not in element:
        continue

    tags = element.get('tags', {})

    cursor.execute("""
        INSERT INTO subway_stations (id, name, lat, lon)
        VALUES (%s, %s, %s, %s)
    """, (
        element['id'],
        tags.get('name'),
        element['lat'],
        element['lon']
    ))

conn.commit()
cursor.close()
conn.close()

print("Done. Stations loaded:", len(data['elements']))