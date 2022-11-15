from mapbox import Geocoder
import json

geocoder = Geocoder(
    access_token="pk.eyJ1IjoiZ3NvbWl0ZmFocmVyZGIiLCJhIjoiY2xhaThmaGw3MDA3cjN2cGdvcXoyaGJjNyJ9.njwSq8e35577L6DyujSyKQ"
)


def get_mapbox_placename(adress_to_search):
    response = geocoder.forward(adress_to_search, limit=1)
    first = response.geojson()["features"][0]
    return first["place_name"]


def get_mapbox_coordinates(adress_to_search):
    response = geocoder.forward(adress_to_search, limit=1)
    print(json.dumps(response.geojson()))
    first = response.geojson()["features"][0]
    coordinates = {}
    coordinates["latitude"] = first["geometry"]["coordinates"][1]
    coordinates["longitude"] = first["geometry"]["coordinates"][0]
    place_name = first["place_name"]
    return coordinates, place_name


def get_mapbox_adress(lon, lat):
    response = geocoder.reverse(lon=lon, lat=lat)
    first = response.geojson()["features"][0]
    return first["place_name"]
