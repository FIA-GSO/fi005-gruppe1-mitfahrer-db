from geopy.distance import geodesic as GD
from lib.AdressConverter import get_mapbox_coordinates


def get_distance_of_two_adresses(first_adress, second_adress):
    first_coordinates = get_mapbox_coordinates(first_adress)
    second_coordinates = get_mapbox_coordinates(second_adress)
    distance = GD(
        (first_coordinates["latitude"], first_coordinates["longitude"]),
        (second_coordinates["latitude"], second_coordinates["longitude"]),
    )
    return round(distance.km, 1)
