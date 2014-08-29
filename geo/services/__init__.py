from geo.services.geocode import GeocodeService
from geo.services.reverse import ReverseGeocodeService


class EchoService(object):
    def get(self, data):
        return data


registry = {
    "/geocode/": GeocodeService,
    "/reverse/": ReverseGeocodeService,
    "/echo/": EchoService
}
