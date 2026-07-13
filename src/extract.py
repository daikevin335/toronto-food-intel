import requests
import json
from pathlib import Path

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# --- Restaurant Query ---

restaurant_query = """
[out:json];

(
  node["amenity"~"restaurant|cafe|fast_food|bar|pub|ice_cream"](43.55,-79.65,43.85,-79.10);
  way["amenity"~"restaurant|cafe|fast_food|bar|pub|ice_cream"](43.55,-79.65,43.85,-79.10);
  relation["amenity"~"restaurant|cafe|fast_food|bar|pub|ice_cream"](43.55,-79.65,43.85,-79.10);
);

out center;
"""

# --- Subway Station Query --- 

subway_query = """
[out:json];
(
    node["station"="subway"](43.60,-79.70,43.90,-79.10);
);
out center;
"""

headers = {
    "User-Agent": "toronto-food-intel (kevin.dai@student)"
}

# --- Pull Restaurants  ---

print("Fetching restaurant...")
response = requests.get(
    OVERPASS_URL,
    params={"data": restaurant_query},
    headers=headers
)

if response.status_code != 200:
    print("ERROR:", response.status_code)
    print(response.text[:500])
    exit()

data = response.json()
print(f"Restaurant count: {len(data['elements'])}")

output_path = Path("data/raw/restaurants.json")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

print("Done. Data saved to data/raw/restaurants.json")

# --- Pull Subway Stations ---

print("\nFetching subway stations...")
response = requests.post(
    OVERPASS_URL,
    data={"data": subway_query},
    headers=headers
)

if response.status_code != 200:
    print("ERROR:", response.status_code)
    exit()

data = response.json()
print(f"Subway Station count: {len(data['elements'])}")

output_path = Path("data/raw/subway_stations.json")
with open(output_path, "w") as f:
    json.dump(data, f, indent = 2)
print("Saved to data/raw/subway_stations.json")
