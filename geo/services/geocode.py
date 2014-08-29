from geo.requestlib import AbortException
from geo.services.connections import get_tiger_db_conn


class GeocodeService(object):
    def get(self, data):
        if "location" not in data:
            raise AbortException(400, "location string required")
        return geocode_tiger(data["location"])


def geocode_tiger(location_string):
    """
    Geocodes a given location string and returns either a dictionary of it's
    coordinates or None
    """
    query = "SELECT g.rating," \
            " ST_X(g.geomout) AS longitude," \
            " ST_Y(g.geomout) AS latitude," \
            " (addy).address AS street_num," \
            " (addy).streetname AS street_name," \
            " (addy).streettypeabbrev AS street_type," \
            " (addy).location AS city," \
            " (addy).stateabbrev AS region," \
            " (addy).zip AS postal_code " \
            "FROM geocode(%s, 1) AS g;"

    # SQL implementing geocode() does not sanitize its inputs properly
    rev_location_string = location_string.replace(
        '(', '\\(').replace(')', '\\)')

    # Execute the geocode query
    conn = get_tiger_db_conn()
    cursor = conn.cursor()
    cursor.execute(query, [rev_location_string])
    result = cursor.fetchone()

    # Must match columns in "query", defined above
    if result:
        (rating, longitude, latitude, street_num, street_name, street_type,
         city, region, postal_code) = result

        if latitude and longitude:
            return {
                "rating": rating,
                "street": "%s %s %s" % (street_num, street_name, street_type),
                "city": city,
                "region": region,
                "postal_code": postal_code,
                "latitude": latitude,
                "longitude": longitude
            }
