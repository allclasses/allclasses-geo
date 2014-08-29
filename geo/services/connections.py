import gevent_psycopg2
gevent_psycopg2.monkey_patch()

from psycopg2.pool import ThreadedConnectionPool

import geo.settings as settings


TIGER_DB_CONNECTION_POOL = ThreadedConnectionPool(
    settings.POSTGIS_TIGER_MIN_CONNECTIONS,
    settings.POSTGIS_TIGER_MAX_CONNECTIONS,
    settings.POSTGIS_TIGER_DSN
)


def get_tiger_db_conn():
    return TIGER_DB_CONNECTION_POOL.getconn()


def put_tiger_db_conn(conn):
    return TIGER_DB_CONNECTION_POOL.putconn(conn)
