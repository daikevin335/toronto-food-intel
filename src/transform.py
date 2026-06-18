import json 

# Load raw data
with open("data/raw/restaurants.json") as f:
    data = json.load(f)

restaurants = []

# Loop through every restaurants 
for element in data["elements"]:

    tags = element.get("tags", {})

    # Hande coordinates 
    if "lat" in element: 
        lat = element["lat"]
        lon = element["lon"]
    else:
        lat = element["center"]["lat"]
        lon = element["center"]["lon"]
    
    restaurant = {
        "osm_id": element["id"],
        "name": tags.get("name"),
        "category": tags.get("amenity"),
        "cuisine": tags.get("cuisine"),
        "latitude": lat, 
        "longitude": lon,
        "street": tags.get("addr:street"),
        "city": tags.get("addr:city")
    }
  
    restaurants.append(restaurant)

print("Transformed:", len(restaurants))

print(restaurants[0])

print(type(data))
print(type(data["elements"]))
print(len(data["elements"]))