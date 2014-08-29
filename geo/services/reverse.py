from geo.requestlib import AbortException
from geo.services.connections import get_tiger_db_conn


class ReverseGeocodeService(object):
    def get(self, data):
        if not (isinstance(data.get("latitude"), float) and
                isinstance(data.get("longitude"), float)):
            raise AbortException(400, "lat/lon must be floats")
        return reverse_geocode_tiger(data["latitude"], data["longitude"])


def reverse_geocode_tiger(latitude, longitude):
    """
    Geocodes a given location string and returns either a dictionary of it's
    coordinates or None
    """
    query = "SELECT " \
            " r.addy[1].address AS street_num," \
            " r.addy[1].streetname AS street_name," \
            " r.addy[1].streettypeabbrev AS street_type," \
            " r.addy[1].location AS city," \
            " r.addy[1].stateabbrev AS region," \
            " r.addy[1].zip AS postal_code " \
            "FROM reverse_geocode(" \
            "ST_GeomFromText('POINT(%s %s)', 4269), true) " \
            "AS r;"

    # Execute the geocode query
    conn = get_tiger_db_conn()
    cursor = conn.cursor()
    cursor.execute(query, [longitude, latitude])
    result = cursor.fetchone()

    # Must match columns in "query", defined above
    if result:
        (street_num, street_name, street_type,
         city, region, postal_code) = result

        if street_num and street_name:
            return {
                "rating": None,
                "street": "%s %s %s" % (street_num, street_name, street_type),
                "city": city,
                "region": region,
                "postal_code": postal_code,
                "latitude": latitude,
                "longitude": longitude
            }
