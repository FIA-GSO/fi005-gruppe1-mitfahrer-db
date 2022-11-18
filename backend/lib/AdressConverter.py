from mapbox import Geocoder
import json
from .custom_geocoding import custom_reverse
import os

geocoder = Geocoder(access_token=os.getenv("MAPBOX_API_KEY"))
geocoder.reverse = lambda *args, **kwargs: custom_reverse(geocoder, *args, **kwargs)


def get_mapbox_placename(adress_to_search):
    response = geocoder.forward(adress_to_search, limit=1)
    first = response.geojson()["features"][0]
    return first["place_name"]


def get_mapbox_coordinates(adress_to_search, languages=["de"]):
    response = geocoder.forward(adress_to_search, limit=1, languages=languages)
    first = response.geojson()["features"][0]
    coordinates = {}
    coordinates["latitude"] = first["geometry"]["coordinates"][1]
    coordinates["longitude"] = first["geometry"]["coordinates"][0]
    place_name = first["place_name"]
    return coordinates, place_name


def get_mapbox_adress(lon, lat, languages=["de"]):
    response = geocoder.reverse(lon=lon, lat=lat, languages=languages)
    first = response.geojson()["features"][0]
    return first["place_name"]


if __name__ == "__main__":
    print(get_mapbox_adress(6.999419967047289, 50.92057473086024))
