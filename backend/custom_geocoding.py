from mapbox.errors import InvalidPlaceTypeError
from uritemplate import URITemplate


def custom_reverse(self, lon, lat, types=None, limit=None, languages=None):
    """Returns a Requests response object that contains a GeoJSON
    collection of places near the given longitude and latitude.

    `response.geojson()` returns the geocoding result as GeoJSON.
    `response.status_code` returns the HTTP API status code.

    See: https://www.mapbox.com/api-documentation/search/#reverse-geocoding."""
    uri = URITemplate(self.baseuri + "/{dataset}/{lon},{lat}.json").expand(
        dataset=self.name,
        lon=str(round(float(lon), self.precision.get("reverse", 5))),
        lat=str(round(float(lat), self.precision.get("reverse", 5))),
    )
    params = {}

    if types:
        types = list(types)
        params.update(self._validate_place_types(types))
    if languages:
        params.update(language=",".join(languages))
    if limit is not None:
        if not types or len(types) != 1:
            raise InvalidPlaceTypeError(
                "Specify a single type when using limit with reverse geocoding"
            )
        params.update(limit="{0}".format(limit))

    resp = self.session.get(uri, params=params)
    self.handle_http_error(resp)

    # for consistency with other services
    def geojson():
        return resp.json()

    resp.geojson = geojson

    return resp
