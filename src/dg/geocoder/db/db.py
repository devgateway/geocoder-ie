import psycopg2
from dg.geocoder.config import get_db_name, get_user_name, get_password


def open():
    try:
        conn = psycopg2.connect(
            'dbname={db_name} user={user_name} password={password}'.format(db_name=get_db_name(), user_name=get_user_name(),
                                                                           password=get_password()))
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print("Wasn't able to connect")
        raise


def close(conn):
    if conn is not None:
        try:
            conn.close()
        except (Exception, psycopg2.Error) as error:
            print('error when closing connection')
