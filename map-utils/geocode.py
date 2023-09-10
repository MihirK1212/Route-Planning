
import pandas as pd
import json
import numpy as np
import googlemaps

GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

def get_coordinate(address : str):
    try:
        geocode_result = gmaps.geocode(address)
        lat , lng = geocode_result[0]['geometry']['location']['lat'],geocode_result[0]['geometry']['location']['lng']
        return {
        'lat' : lat,
        'lng' : lng
        }
    except Exception as E:
        print(E)
        print("Could not find for ",address)


items_dispatch = pd.read_csv("./items_dispatch.csv")
items_pickup   = pd.read_csv("./items_pickup.csv")

addresses_dispatch , awb_dispatch = list(items_dispatch["address"]) , list(items_dispatch["AWB"])
addresses_pickup , awb_pickup = list(items_pickup["address"]) , list(items_pickup["AWB"])

awb_to_coordinate = dict()

for i in range(len(addresses_dispatch)):
    address = addresses_dispatch[i]
    if str(address) == "nan":
        continue
    else:
        awb_to_coordinate[str(int(awb_dispatch[i]))] = get_coordinate(address)
    
for i in range(len(addresses_pickup)):
    address = addresses_pickup[i]
    if str(address) == "nan":
        continue
    else:
        awb_to_coordinate[str(int(awb_pickup[i]))] = get_coordinate(address)

with open("./awb_to_coordinate_temp.json", "w") as outfile:
    json.dump(awb_to_coordinate, outfile)