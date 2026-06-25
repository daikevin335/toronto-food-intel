import json
import psycopg2

# Load raw JSON
with open('data/raw/restaurants.json') as f:
    data = json.load(f)

# Connect to PostgreSQL

conn = psycopg2.connect( # Live link between Python Scripy & Database 
    host = "localhost",
    database = "toronto_food_analytics",
    user = "kevindai"
)

cursor = conn.cursor() # Other end of Live Link channel to send to SQL

print("Connected. Records to load:", len(data['elements']))

# Loop through every restaurant
for element in data['elements']:

    # Skip elements without coords
    if 'lat' not in element or 'lon' not in element:
        continue

    tags = element.get('tags', {})
    
    cursor.execute("""
        INSERT INTO restaurants (
            id, name, cuisine, amenity,
            housenumber, street, city,
            lat, lon, phone
        ) VALUES (
            %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s
        )
        """, 
        (
        element['id'],
        tags.get('name'),
        tags.get('cuisine'),
        tags.get('amenity'),
        tags.get('addr:housenumber'),
        tags.get('addr:street'),
        tags.get('addr:city'),
        element['lat'],
        element['lon'],
        tags.get('phone')
    ))

# Save everything
conn.commit()
cursor.close()
conn.close()

print("Completed. Rows loaded:", len(data['elements']))