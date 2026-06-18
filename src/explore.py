import json 

with open("data/raw/restaurants.json") as f:
    data = json.load(f)


total = len(data["elements"])

with_name = 0   
with_cuisine = 0    

for element in data["elements"]:

    tags = element.get("tags", {})

    if "name" in tags:
        with_name += 1 
    
    if "cuisine" in tags:
        with_cuisine += 1 

print("Total records:", total)
print("Has name:", with_name)
print("Has cuisine:", with_cuisine)


first = data["elements"][0]

print(type(first))
print(first)