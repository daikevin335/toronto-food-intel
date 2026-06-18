import requests
import json
from pathlib import Path

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

query = """
[out:json];

(
  node["amenity"~"restaurant|cafe|fast_food|bar|pub|ice_cream"](43.55,-79.65,43.85,-79.10);
  way["amenity"~"restaurant|cafe|fast_food|bar|pub|ice_cream"](43.55,-79.65,43.85,-79.10);
  relation["amenity"~"restaurant|cafe|fast_food|bar|pub|ice_cream"](43.55,-79.65,43.85,-79.10);
);

out center;
"""

headers = {
    "User-Agent": "hidden-toronto-project (kevin.dai@student)",
    "Accept": "application/json"
}

response = requests.get(
    OVERPASS_URL,
    params={"data": query},
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